from pydantic import BaseModel
from datetime import date
from typing import Literal

class DocumentBase(BaseModel):
    doc_type: Literal["passport", "id_card", "driver_license"]
    expiry_date: date
    file_path: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True
