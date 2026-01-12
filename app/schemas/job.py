from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime,date

class JobCreate(BaseModel):
    title: str
    department: str
    work_mode: Optional[str]
    roles_responsibilities: Optional[str]
    required_skills: Optional[str]
    experience_min: Optional[int]
    experience_max: Optional[int]
    qualification_required: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    perks_benefits: Optional[str]
    job_summary: Optional[str]
    job_location: Optional[str]
    job_locality: Optional[str]
    openings: Optional[int]
    application_deadline: Optional[date]


class JobUpdate(BaseModel):
    title: Optional[str]
    department: Optional[str]
    work_mode: Optional[str]

    roles_responsibilities: Optional[str]
    required_skills: Optional[str]

    experience_min: Optional[int]
    experience_max: Optional[int]

    qualification_required: Optional[str]

    salary_min: Optional[int]
    salary_max: Optional[int]

    perks_benefits: Optional[str]
    job_summary: Optional[str]

    job_location: Optional[str]
    job_locality: Optional[str]

    openings: Optional[int]
    application_deadline: Optional[date]
    is_active: Optional[bool]


class JobResponse(JobCreate):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

'''
class JobOut(BaseModel):
    id: int
    title: str
    department: str
    location: str
    employment_type: str
    experience: str
    description: str
    jd_file: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True'''

class PaginatedJobResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[JobResponse]

    

    
