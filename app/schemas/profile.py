from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.schemas.address import AddressCreate, AddressResponse
from app.schemas.contact import ContactCreate, ContactResponse
from app.schemas.employment import EmploymentCreate, EmploymentResponse
from app.schemas.document import DocumentCreate, DocumentResponse

class ProfileBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    dob: date
    age: Optional[int] = None

class ProfileCreate(ProfileBase):
    addresses: List[AddressCreate] = []
    contacts: List[ContactCreate] = []
    employments: List[EmploymentCreate] = []
    documents: DocumentCreate


class ProfileUpdate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    dob: date
    age: Optional[int] = None
    addresses: Optional[List[AddressCreate]] = None
    contacts: Optional[List[ContactCreate]] = None
    employments: Optional[List[EmploymentCreate]] = None
    documents: DocumentCreate


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    addresses: List[AddressResponse] = []
    contacts: List[ContactResponse] = []
    documents: DocumentResponse
    employments: List[EmploymentResponse] = []

    class Config:
        from_attributes = True
