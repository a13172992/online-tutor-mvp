from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EssaySubmission(Base):
    __tablename__ = 'essays'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    score = Column(Integer, nullable=True)
    rubric = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Checkin(Base):
    __tablename__ = 'checkins'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)

class DailyPracticeRecord(Base):
    __tablename__ = 'daily_practices'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)
    date = Column(Date, index=True, nullable=False)
    content = Column(Text, nullable=False)  # JSON string of the daily content/responses
    created_at = Column(DateTime, default=datetime.utcnow)
