from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func, extract
from datetime import datetime, date
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/api", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stats", response_model=schemas.FeedbackStats)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(models.Feedback).count()
    avg_rating = db.query(sa_func.avg(models.Feedback.rating)).scalar() or 0.0
    today = db.query(models.Feedback).filter(
        sa_func.date(models.Feedback.created_at) == date.today()
    ).count()

    return schemas.FeedbackStats(total=total, avg_rating=round(avg_rating, 2), today=today)
