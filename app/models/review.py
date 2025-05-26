from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ReviewStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.pending)
    comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="reviews_received")
    officer = relationship("User", foreign_keys=[officer_id], back_populates="reviews_created")