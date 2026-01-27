from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional


# -------------------------------------------------------------------
# BASE SCHEMA
# -------------------------------------------------------------------
class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    phone: str
    email: str
    date_of_birth: date
    gender: str
    location: str

    pan_number: str
    linkedin_url: Optional[str] = None

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

    experience_level: str  # "fresher" | "experienced"

    previous_company: Optional[str] = None
    previous_role: Optional[str] = None
    date_of_joining: Optional[date] = None
    relieving_date: Optional[date] = None

    job_id: int

    # --------------------------------------------------
    # EXPERIENCE VALIDATION
    # --------------------------------------------------
    @field_validator(
        "previous_company",
        "previous_role",
        "date_of_joining",
        "relieving_date",
        mode="after",
    )
    @classmethod
    def validate_experience_fields(cls, v, info):
        experience_level = info.data.get("experience_level")

        if experience_level == "experienced" and v is None:
            raise ValueError(
                "previous_company, previous_role, date_of_joining and relieving_date "
                "are required for experienced candidates"
            )

        # Fresher → these fields are optional
        return v


# -------------------------------------------------------------------
# CREATE SCHEMA
# -------------------------------------------------------------------
class ApplicationCreate(ApplicationBase):
    pass


# -------------------------------------------------------------------
# RESPONSE SCHEMA (⚠ MUST MATCH DB COLUMN NAMES)
# -------------------------------------------------------------------
class ApplicationResponse(ApplicationBase):
    id: int

    # 🔥 MUST MATCH SQLAlchemy MODEL / DB
    pan_card_file: Optional[str]
    resume_file: Optional[str]
    photo_file: Optional[str]

    status: str
    created_at: datetime
