from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(100), default="Аноним")
    rating = Column(Integer)
    category = Column(String(50), default="other")
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_read = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )
