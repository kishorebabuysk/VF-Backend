from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic import BaseModel
from typing import Optional,List
from datetime import date


class JobApplicationCreate(BaseModel):
    #first_name: str
    #last_name: str
    full_name: str
    phone: str
    email: str
    date_of_birth: date
    gender: str
    location: str

    pan_number: str
    linkedin_url: Optional[str]

    highest_qualification: str
    specialization: str
    university: str
    college: str
    year_of_passing: int

    position_applied: str
    preferred_work_mode: str
    key_skills: str
    expected_salary: int
    why_hire_me: str

    experience_level: str  # Fresher / Experienced

    # Experienced-only
    previous_company: Optional[str]
    previous_role: Optional[str]
    date_of_joining: Optional[date]
    relieving_date: Optional[date]

    captcha_verified: bool



class JobApplicationDetailResponse(BaseModel):
    id: int

    #first_name: str
    #last_name: str
    full_name : str
    phone: str
    email: EmailStr
    date_of_birth: date
    gender: str
    location: str

    pan_number: str
    linkedin_url: Optional[str]

    highest_qualification: str
    specialization: str
    university: str
    college: str
    year_of_passing: int

    position_applied: str
    preferred_work_mode: str
    key_skills: str
    expected_salary: int
    why_hire_me: str

    experience_level: str

    previous_company: Optional[str]
    previous_role: Optional[str]
    date_of_joining: Optional[date]
    relieving_date: Optional[date]

    created_at: datetime

    class Config:
        from_attributes = True

class BulkDeleteRequest(BaseModel):
    application_ids: List[int]
