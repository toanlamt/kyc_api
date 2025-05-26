from pydantic import BaseModel, Field
from decimal import Decimal


class WealthSourceBase(BaseModel):
    source_type: str
    amount: Decimal = Field(..., gt=0)
    currency: str = "USD"

class WealthSourceCreate(WealthSourceBase):
    pass

class WealthSourceResponse(WealthSourceBase):
    id: int

    class Config:
        orm_mode = True