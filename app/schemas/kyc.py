from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.asset import AssetCreate, AssetResponse
from app.schemas.liability import LiabilityCreate, LiabilityResponse
from app.schemas.income import IncomeCreate, IncomeResponse
from app.schemas.wealth_source import WealthSourceCreate, WealthSourceResponse


class KYCBase(BaseModel):
    market_experience: str
    risk_tolerance: str

class KYCCreate(KYCBase):
    incomes: List[IncomeCreate] = []
    assets: List[AssetCreate] = []
    liabilities: List[LiabilityCreate] = []
    wealth_sources: List[WealthSourceCreate] = []

class KYCUpdate(BaseModel):
    market_experience: Optional[str] = None
    risk_tolerance: Optional[str] = None
    incomes: Optional[List[IncomeCreate]] = None
    assets: Optional[List[AssetCreate]] = None
    liabilities: Optional[List[LiabilityCreate]] = None
    wealth_sources: Optional[List[WealthSourceCreate]] = None

class KYC(KYCBase):
    id: int
    user_id: int
    total_income: Decimal
    total_assets: Decimal
    total_liabilities: Decimal
    total_wealth_source: Decimal
    net_worth: Decimal
    incomes: List[IncomeResponse] = []
    assets: List[AssetResponse] = []
    liabilities: List[LiabilityResponse] = []
    wealth_sources: List[WealthSourceResponse] = []
    created_at: datetime

    class Config:
        orm_mode = True