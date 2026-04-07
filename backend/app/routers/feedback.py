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


async def notify_telegram(message: str, rating: int, author: str, category: str, fb_id: int):
    """Отправка уведомления в Telegram с кнопкой удаления"""
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        return

    cat_emoji = {"coffee": "☕", "service": "🤝", "atmosphere": "🏠", "other": "📝"}.get(category, "📝")
    stars = "⭐" * rating if rating else ""

    text = f"☕ *Новый отзыв!*\n\n"
    text += f"{cat_emoji} *Автор:* {author}\n"
    if rating:
        text += f"⭐ *Оценка:* {rating}/5\n"
    text += f"💬 *Сообщение:* _{message}_"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    keyboard = {"inline_keyboard": [[{"text": "❌ Удалить", "callback_data": f"delete_{fb_id}"}]]}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={
                "chat_id": ADMIN_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": keyboard,
            })
        except Exception:
            pass


@router.post("", response_model=schemas.FeedbackResponse)
async def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    # Сохранение в БД
    db_feedback = models.Feedback(**feedback.model_dump(exclude_unset=True))
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    # Отправка уведомления в Telegram (после получения ID)
    await notify_telegram(
        feedback.message,
        feedback.rating or 0,
        feedback.author or "Аноним",
        feedback.category or "other",
        db_feedback.id,
    )
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
