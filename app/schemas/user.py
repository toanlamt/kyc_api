from pydantic import BaseModel, Field, field_validator
import re
from app.models.user import RoleEnum

class UserBase(BaseModel):
    username: str = Field(..., min_length=8, max_length=10)
    role: RoleEnum = RoleEnum.user

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if not (12 <= len(v) <= 16):
            raise ValueError("Password must be between 12 and 16 characters.")
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("Password must include letters.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must include numbers.")
        if not re.search(r"[@#&!]", v):
            raise ValueError("Password must include at least one special character (@, #, &, !).")
        return v

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


