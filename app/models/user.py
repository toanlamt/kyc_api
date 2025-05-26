from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class RoleEnum(str, enum.Enum):
    user = "user"
    officer = "officer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)

    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    kyc = relationship("KYC", uselist=False, back_populates="user", cascade="all, delete-orphan")
    # reviews_created = relationship("Review", foreign_keys="Review.officer_id", back_populates="officer")
    # reviews_received = relationship("Review", foreign_keys="Review.user_id", back_populates="user")
