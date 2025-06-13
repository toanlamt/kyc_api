from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.asset import AssetCreate, AssetResponse
from app.schemas.liability import LiabilityCreate, LiabilityResponse
from app.schemas.income import IncomeCreate, IncomeResponse
from app.schemas.wealth_source import WealthSourceCreate, WealthSourceResponse
from app.models.kyc import ExperienceLevel, RiskTolerance, KYCStatus
from datetime import datetime

class KYCBase(BaseModel):
    market_experience: Optional[str]
    risk_tolerance: Optional[str]

class KYCCreate(KYCBase):
    incomes: List[IncomeCreate] = []
    assets: List[AssetCreate] = []
    liabilities: List[LiabilityCreate] = []
    wealth_sources: List[WealthSourceCreate] = []

class KYCUpdate(BaseModel):
    id: int
    user_id: int
    market_experience: Optional[ExperienceLevel] = None
    risk_tolerance: Optional[RiskTolerance] = None
    incomes: Optional[List[IncomeCreate]] = None
    assets: Optional[List[AssetCreate]] = None
    liabilities: Optional[List[LiabilityCreate]] = None
    wealth_sources: Optional[List[WealthSourceCreate]] = None

class KYC(KYCBase):
    id: int
    user_id: int
    status: KYCStatus
    status_updated_at: datetime
    incomes: Optional[List[IncomeResponse]] = []
    assets: Optional[List[AssetResponse]] = []
    liabilities: Optional[List[LiabilityResponse]] = []
    wealth_sources: Optional[List[WealthSourceResponse]] = []

    class Config:
        from_attributes = True