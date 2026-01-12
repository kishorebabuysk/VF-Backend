from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CSRCreate(BaseModel):
    title: str
    description: str
    image: Optional[str] = None

class CSRUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image: Optional[str]
    is_active: Optional[bool]

class CSRResponse(BaseModel):
    id: int
    title: str
    description: str
    image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
