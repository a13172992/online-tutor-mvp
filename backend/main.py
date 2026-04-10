from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
import json

app = FastAPI(title="Online Tutor MVP")

# Seed data cache for in-memory demo content (will be combined with persistence in DB)
_seed_cache = seed_data() if 'seed_data' in globals() else {}

"""
Refactored main.py: MVP endpoints now backed by a SQLite DB via SQLAlchemy.
This keeps backward compatibility for the endpoints while enabling persistence.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional
import json

from .database import engine, get_db
from .models import Base, User, EssaySubmission, Checkin, DailyPracticeRecord

from .seed_data import seed as seed_data

app = FastAPI(title="Online Tutor MVP")

# Simple in-memory cache-like data to seed initial content when DB is empty
_seed_cache = seed_data()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Initialize with sample data in memory for demo; DB-backed data is primarily used for persistence
    pass

class AnalyzeRequest(BaseModel):
    sentence: str


class EssayRequest(BaseModel):
    title: Optional[str] = None
    text: str


class CheckinRequest(BaseModel):
    user_id: str


@app.post("/analyze-long-sentence")
async def analyze_long_sentence(req: AnalyzeRequest):
    s = req.sentence.strip()
    if not s:
        raise HTTPException(status_code=400, detail="Empty sentence")

    clauses = [cl.strip() for cl in s.replace("，", ",").split(",") if cl.strip()]
    structure = {
        "original": s,
        "clauses_count": len(clauses),
        "core_idea": clauses[0] if clauses else s
    }

    exercises = []
    for i, cl in enumerate(clauses[:5]):
        ex = f"练习 {i+1}: 将子句 '{cl}' 改写为同义表达，保持原句逻辑关系。"
        exercises.append({"prompt": ex, "example": cl})

    if not exercises:
        exercises = [{"prompt": "练习 1: 对该句进行改写练习。", "example": s}]

    return {"analysis": structure, "exercises": exercises[:5]}


@app.post("/grade-essay")
async def grade_essay(req: EssayRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty essay")

    words = text.split()
    wc = len(words)
    sentences = max(1, text.count(".") + text.count("!") + text.count("?"))
    avg_len = wc / sentences if sentences else 0

    content_score = min(40, max(5, int((wc / 5))))
    structure_score = min(30, max(5, int((sentences / 2) * 5)))
    language_score = min(25, max(0, int((wc / 3))))
    mechanics_score = max(5, 100 - wc // 50)
    total = max(0, min(100, content_score + structure_score + language_score + mechanics_score))

    feedback = []
    if wc < 150:
        feedback.append("篇幅较短，需扩展论点与例证。")
    if avg_len > 20:
        feedback.append("句子过长，建议适当拆分。")
    if " however" in text or " but" in text:
        feedback.append("尝试更自然的转折连接词以提升连贯性。")
    if not feedback:
        feedback.append("结构清晰，语言通顺。")

    # Persist to DB
    from .database import SessionLocal
    from datetime import datetime as dt
    db = SessionLocal()
    try:
        essay = EssaySubmission(
            title=req.title,
            text=text,
            score=int(total),
            rubric=json.dumps({"content": int(content_score), "structure": int(structure_score), "language": int(language_score), "mechanics": int(mechanics_score)}),
            feedback="; ".join(feedback),
            created_at=dt.utcnow(),
        )
        db.add(essay)
        db.commit()
        db.refresh(essay)
    finally:
        db.close()

    return {
        "essay_id": getattr(essay, 'id', None),
        "score": int(total),
        "rubric": {
            "content": int(content_score),
            "structure": int(structure_score),
            "language": int(language_score),
            "mechanics": int(mechanics_score)
        },
        "feedback": feedback
    }


@app.post("/submit-essay")
async def submit_essay(title: Optional[str] = None, text: Optional[str] = None):
    if text is None:
        raise HTTPException(status_code=400, detail="Essay text required")
    # Reuse grade_essay logic and persist
    res = await grade_essay(EssayRequest(title=title, text=text))
    return {"title": title, "content_preview": (text[:200] + ("..." if len(text) > 200 else "")), "grade": res}


@app.get("/daily-practice")
async def daily_practice(user_id: Optional[str] = None):
    today = date.today()
    eng5 = _seed_cache.get("english_sentences", [])[:5]
    chi5 = _seed_cache.get("chinese_sentences", [])[:5]
    quote = _seed_cache.get("daily_quotes", [])[today.day % max(1, len(_seed_cache.get("daily_quotes", [])))]

    data = {
        "date": today.isoformat(),
        "daily_quote": quote,
        "english_to_chinese": [{"id": i+1, "prompt": eng5[i], "answer": chi5[i] if i < len(chi5) else ""} for i in range(len(eng5))],
        "chinese_to_english": [{"id": i+1, "prompt": chi5[i], "answer": eng5[i] if i < len(eng5) else ""} for i in range(len(chi5))],
        "model_essays": _seed_cache.get("gaokao_model_essays", [])
    }

    # Persist daily content usage for the user (optional)
    if user_id:
        from .database import SessionLocal
        db = SessionLocal()
        try:
            rec = DailyPracticeRecord(
                user_id=user_id,
                date=today,
                content=json.dumps(data)
            )
            db.add(rec)
            db.commit()
            db.refresh(rec)
        finally:
            db.close()
    return data


@app.post("/checkin")
async def checkin(req: CheckinRequest):
    user = req.user_id
    if not user:
        raise HTTPException(status_code=400, detail="user_id required")
    today = date.today()
    from .database import SessionLocal
    db = SessionLocal()
    try:
        existing = db.query(Checkin).filter(Checkin.user_id == user, Checkin.date == today).first()
        if existing:
            return {"status": "already_checked_in", "date": today.isoformat()}
        ci = Checkin(user_id=user, date=today, checked_at=datetime.utcnow())
        db.add(ci)
        db.commit()
        return {"status": "checked_in", "date": today.isoformat()}
    finally:
        db.close()


@app.get("/model-essays")
async def get_model_essays():
    return _seed_cache.get("gaokao_model_essays", [])


@app.get("/quotes")
async def get_quotes():
    return _seed_cache.get("daily_quotes", [])


@app.get("/health")
async def health():
    return {"status": "ok"}
