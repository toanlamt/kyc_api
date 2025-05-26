from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class IncomeType(str, enum.Enum):
    salary = "salary"
    investment = "investment"
    others = "others"

class Income(Base):
    __tablename__ = "incomes"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(Integer, ForeignKey("kyc.id"), nullable=False)
    income_type = Column(Enum(IncomeType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String, default="USD")
    
    kyc = relationship("KYC", back_populates="incomes")
