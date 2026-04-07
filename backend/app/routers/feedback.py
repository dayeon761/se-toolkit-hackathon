from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import SessionLocal
import httpx
import os

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def notify_telegram(message: str, rating: int, author: str):
    """Отправка уведомления в Telegram"""
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        return
    
    text = f"☕ Новый отзыв!\n\n"
    text += f"👤 Автор: {author}\n"
    if rating:
        text += f"⭐ Оценка: {rating}/5\n"
    text += f"💬 Сообщение: {message}"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={"chat_id": ADMIN_CHAT_ID, "text": text})
        except Exception:
            pass  # Не прерываем создание отзыва при ошибке уведомления


@router.post("", response_model=schemas.FeedbackResponse)
async def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    # Отправка уведомления в Telegram
    await notify_telegram(feedback.message, feedback.rating or 0, feedback.author or "Аноним")
    
    # Сохранение в БД
    db_feedback = models.Feedback(**feedback.model_dump(exclude_unset=True))
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("", response_model=List[schemas.FeedbackResponse])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()


@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    db.delete(db_feedback)
    db.commit()
    return {"message": "Отзыв удален"}


@router.put("/{feedback_id}/read")
def mark_as_read(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    db_feedback.is_read = True
    db.commit()
    db.refresh(db_feedback)
    return {"message": "Отзыв отмечен как прочитанный"}
