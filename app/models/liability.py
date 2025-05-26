from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class LiabilityType(str, enum.Enum):
    personal_loan = "personal_loan"
    real_estate_loan = "real_estate_loan"
    others = "others"

class Liability(Base):
    __tablename__ = "liabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(Integer, ForeignKey("kyc.id"), nullable=False)
    liability_type = Column(Enum(LiabilityType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String, default="USD")
    
    kyc = relationship("KYC", back_populates="liabilities")
