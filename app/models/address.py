from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class AddressType(str, enum.Enum):
    mailing = "mailing"
    work = "work"

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))

    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)

    type = Column(Enum(AddressType), nullable=False)

    profile = relationship("Profile", back_populates="addresses")
