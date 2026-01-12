from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactResponse(ContactCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BulkDeleteRequest(BaseModel):
    contact_ids: List[int]
