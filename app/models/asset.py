from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class AssetType(str, enum.Enum):
    bond = "bond"
    liquidity = "liquidity"
    real_estate = "real_estate"
    others = "others"

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    kyc_id = Column(Integer, ForeignKey("kyc.id"), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String, default="USD")
    
    kyc = relationship("KYC", back_populates="assets")
