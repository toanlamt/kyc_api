from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ExperienceLevel(str, enum.Enum):
    less_than_5 = "less_than_5"
    between_5_10 = "between_5_10"
    more_than_10 = "more_than_10"

class RiskTolerance(str, enum.Enum):
    low = "10"
    medium = "30"
    high = "all_in"

class KYC(Base):
    __tablename__ = "kyc"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Investment Experience
    market_experience = Column(Enum(ExperienceLevel), nullable=False)
    risk_tolerance = Column(Enum(RiskTolerance), nullable=False)
    
    # Calculated Net Worth
    total_income = Column(Numeric(15, 2), default=0)
    total_assets = Column(Numeric(15, 2), default=0)
    total_liabilities = Column(Numeric(15, 2), default=0)
    total_wealth_source = Column(Numeric(15, 2), default=0)
    net_worth = Column(Numeric(15, 2), default=0)
    
    # Relationships
    user = relationship("User", back_populates="kyc")
    incomes = relationship("Income", back_populates="kyc", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="kyc", cascade="all, delete-orphan")
    liabilities = relationship("Liability", back_populates="kyc", cascade="all, delete-orphan")
    wealth_sources = relationship("WealthSource", back_populates="kyc", cascade="all, delete-orphan")




