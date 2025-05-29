from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmploymentBase(BaseModel):
    company_name: str
    from_date: date
    to_date: Optional[date] = None

class EmploymentCreate(EmploymentBase):
    pass

class EmploymentResponse(EmploymentBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True
