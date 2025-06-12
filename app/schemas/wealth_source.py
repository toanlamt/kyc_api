from pydantic import BaseModel, Field
from decimal import Decimal


class WealthSourceBase(BaseModel):
    source_type: str
    amount: Decimal = Field(..., gt=0)
    
class WealthSourceCreate(WealthSourceBase):
    pass

class WealthSourceResponse(WealthSourceBase):
    id: int

    class Config:
        from_attributes = True