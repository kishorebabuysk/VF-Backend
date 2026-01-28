from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    department: str
    work_mode: str
    roles_responsibilities: str
    required_skills: str
    experience_min: int
    experience_max: int
    qualification_required: str
    salary_min: int
    salary_max: int
    perks_benefits: Optional[str]
    job_location: str
    job_locality: Optional[str]
    openings: int
    application_deadline: date



class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedJobResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[JobResponse]
