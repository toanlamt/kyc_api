from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class DocumentType(str, enum.Enum):
    passport = "passport"
    id_card = "id_card"
    driver_license = "driver_license"

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    doc_type = Column(Enum(DocumentType), nullable=False)
    expiry_date = Column(Date, nullable=False)
    file_path = Column(String, nullable=False)

    profile = relationship("Profile", back_populates="documents")
