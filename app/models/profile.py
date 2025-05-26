from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    age = Column(Integer)

    user = relationship("User", back_populates="profile")
    contacts = relationship("Contact", back_populates="profile", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="profile", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="profile", cascade="all, delete-orphan")
    employments = relationship("Employment", back_populates="profile", cascade="all, delete-orphan")


