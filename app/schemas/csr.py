from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CSRCreate(BaseModel):
    title: str
    description: str
    image: Optional[str] = None

class CSRUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None


class CSRResponse(BaseModel):
    id: int
    title: str
    description: str
    image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
