from pydantic import BaseModel, field_validator
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

class ProfileBasic(ProfileBase):
    id: int
    user_id: int

class ProfileCreate(BaseModel):
    basicinfo: ProfileBase
    addresses: List[AddressCreate] = []
    contacts: List[ContactCreate] = []
    employments: List[EmploymentCreate] = []
    documents: List[DocumentCreate] = []

    @field_validator("documents")
    def validate_documents(cls, value):
        if not value or len(value) == 0:
            raise ValueError("At least one document must be added.")
        return value


class ProfileUpdate(BaseModel):
    user_id: int
    basicinfo: ProfileBase
    addresses: Optional[List[AddressCreate]] = None
    contacts: Optional[List[ContactCreate]] = None
    employments: Optional[List[EmploymentCreate]] = None
    documents: Optional[List[DocumentCreate]] = None

    @field_validator("documents")
    def validate_documents(cls, value):
        if not value or len(value) == 0:
            raise ValueError("At least one document must be added.")
        return value


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    basicinfo: ProfileBase
    addresses: List[AddressResponse] = []
    contacts: List[ContactResponse] = []
    documents: List[DocumentResponse] = []
    employments: List[EmploymentResponse] = []

    class Config:
        from_attributes = True
