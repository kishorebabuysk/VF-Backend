from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel


class JobBase(BaseModel):
    jobTitle: str
    department: str
    workMode: str
    rolesResponsibilities: str
    requiredSkills: str
    experienceMin: float
    experienceMax: float
    qualification: str
    salaryMin: float
    salaryMax: float
    perksBenefits: Optional[str] = None
    jobLocation: str
    jobLocality: Optional[str] = None
    numOpenings: int
    applicationDeadline: date


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True


class PaginatedJobResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[JobResponse]
