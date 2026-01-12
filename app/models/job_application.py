from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base
'''
class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    resume_file = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, server_default=func.now())'''


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    # Personal Info
    full_name = Column(String(100), nullable=False)
    
    phone = Column(String(20))
    email = Column(String(100))
    date_of_birth = Column(Date)
    gender = Column(String(20))
    location = Column(String(100))

    # Documents
    pan_number = Column(String(20))
    pan_card_file = Column(String(255))
    resume_file = Column(String(255), nullable=False)
    photo_file = Column(String(255))
    linkedin_url = Column(String(255))

    # Education
    highest_qualification = Column(String(100))
    specialization = Column(String(100))
    university = Column(String(150))
    college = Column(String(150))
    year_of_passing = Column(Integer)

    # Job Info
    position_applied = Column(String(150))
    preferred_work_mode = Column(String(50))
    key_skills = Column(Text)
    expected_salary = Column(Integer)
    why_hire_me = Column(Text)

    experience_level = Column(String(50))  # Fresher / Experienced

    # Experienced only
    previous_company = Column(String(150), nullable=True)
    previous_role = Column(String(150), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    relieving_date = Column(Date, nullable=True)

    # Captcha
    captcha_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
