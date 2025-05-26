from pydantic import BaseModel
from typing import Optional

class EmploymentBase(BaseModel):
    company_name: str
    from_year: int
    to_year: Optional[int]

class EmploymentCreate(EmploymentBase):
    pass

class EmploymentResponse(EmploymentBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True
