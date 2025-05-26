from pydantic import BaseModel, Field
from decimal import Decimal

class AssetBase(BaseModel):
    asset_type: str
    amount: Decimal = Field(..., gt=0)
    currency: str = "USD"

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int

    class Config:
        orm_mode = True