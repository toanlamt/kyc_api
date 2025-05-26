from pydantic import BaseModel
from typing import Literal

class ContactBase(BaseModel):
    type: Literal["email", "phone"]
    value: str
    subtype: Literal["work", "personal"]
    preferred: bool = False

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True
