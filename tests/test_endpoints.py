from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_analyze_long_sentence():
    payload = {"sentence": "Despite the rain, the team continued the match with unwavering determination."}
    r = client.post("/analyze-long-sentence", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "analysis" in data
    assert "exercises" in data

def test_register_user():
    r = client.post("/users/register", json={"user_id": "tester"})
    assert r.status_code == 200 or r.status_code == 201
    assert "user_id" in r.json()

def test_daily_practice():
    r = client.get("/daily-practice")
    assert r.status_code == 200
    data = r.json()
    assert "date" in data
    assert "english_to_chinese" in data
