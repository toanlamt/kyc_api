from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class WealthSourceType(str, enum.Enum):
    inheritance = "inheritance"
    donation = "donation"

class WealthSource(Base):
    __tablename__ = "wealth_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(Integer, ForeignKey("kyc.id"), nullable=False)
    source_type = Column(Enum(WealthSourceType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    
    kyc = relationship("KYC", back_populates="wealth_sources")
