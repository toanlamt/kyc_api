from pydantic import BaseModel, Field
from decimal import Decimal


class LiabilityBase(BaseModel):
    liability_type: str
    amount: Decimal = Field(..., gt=0)
    currency: str = "USD"

class LiabilityCreate(LiabilityBase):
    pass

class LiabilityResponse(LiabilityBase):
    id: int

    class Config:
        from_attributes = True