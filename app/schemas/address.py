from pydantic import BaseModel
from typing import Optional, Literal

class AddressBase(BaseModel):
    country: str
    city: str
    street: str
    postal_code: Optional[str] = None
    type: Literal["mailing", "work"]

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True
