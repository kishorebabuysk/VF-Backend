from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime,Date
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    work_mode = Column(String(50))  # Onsite / Hybrid / Remote

    roles_responsibilities = Column(Text)
    required_skills = Column(Text)

    experience_min = Column(Integer)
    experience_max = Column(Integer)

    qualification_required = Column(String(255))

    salary_min = Column(Integer)
    salary_max = Column(Integer)

    perks_benefits = Column(Text)
    job_summary = Column(Text)

    job_location = Column(String(100))
    job_locality = Column(String(100))

    openings = Column(Integer)
    application_deadline = Column(Date)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


'''
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)

    # Keep legacy columns if DB has them
    location = Column(String(100), nullable=True)
    employment_type = Column(String(50), nullable=True)
    experience = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    jd_file = Column(String(255), nullable=True)

    # New fields
    work_mode = Column(String(50), nullable=True)
    roles_responsibilities = Column(Text, nullable=True)
    required_skills = Column(Text, nullable=True)

    experience_min = Column(Integer, nullable=True)
    experience_max = Column(Integer, nullable=True)

    qualification_required = Column(String(255), nullable=True)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)

    perks_benefits = Column(Text, nullable=True)
    job_summary = Column(Text, nullable=True)

    job_location = Column(String(100), nullable=True)
    job_locality = Column(String(100), nullable=True)

    openings = Column(Integer, nullable=True)

    # IMPORTANT: must be Date, not String
    application_deadline = Column(Date, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())'''

