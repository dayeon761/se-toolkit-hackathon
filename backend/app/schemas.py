from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FeedbackCreate(BaseModel):
    author: Optional[str] = "Аноним"
    rating: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[str] = "other"
    message: str = Field(..., min_length=1)


class FeedbackResponse(BaseModel):
    id: int
    author: str
    rating: Optional[int]
    category: str
    message: str
    created_at: datetime
    is_read: bool

    class Config:
        from_attributes = True


class FeedbackStats(BaseModel):
    total: int
    avg_rating: float
    today: int
