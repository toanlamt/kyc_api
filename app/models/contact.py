from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ContactType(str, enum.Enum):
    email = "email"
    phone = "phone"

class ContactSubType(str, enum.Enum):
    work = "work"
    personal = "personal"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))

    type = Column(Enum(ContactType), nullable=False)
    value = Column(String, nullable=False)
    subtype = Column(Enum(ContactSubType), nullable=False)
    preferred = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="contacts")
