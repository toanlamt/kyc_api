from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime

class ExperienceLevel(str, enum.Enum):
    less_than_5 = "less_than_5"
    between_5_10 = "between_5_10"
    more_than_10 = "more_than_10"

class RiskTolerance(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "all_in"

class KYCStatus(str, enum.Enum):
    draft = "Draft"
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

class KYC(Base):
    __tablename__ = "kyc"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Investment Experience
    market_experience = Column(Enum(ExperienceLevel), nullable=True)
    risk_tolerance = Column(Enum(RiskTolerance), nullable=True)


    # KYC status
    status = Column(Enum(KYCStatus), nullable=True, default=KYCStatus.draft)
    status_updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="kyc")
    incomes = relationship("Income", back_populates="kyc", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="kyc", cascade="all, delete-orphan")
    liabilities = relationship("Liability", back_populates="kyc", cascade="all, delete-orphan")
    wealth_sources = relationship("WealthSource", back_populates="kyc", cascade="all, delete-orphan")




