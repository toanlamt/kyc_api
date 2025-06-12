from pydantic import BaseModel, Field
from decimal import Decimal

class IncomeBase(BaseModel):
    income_type: str
    amount: Decimal = Field(..., gt=0)

class IncomeCreate(IncomeBase):
    pass

class IncomeResponse(IncomeBase):
    id: int

    class Config:
        from_attributes = True