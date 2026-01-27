from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Application(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    date_of_birth = Column(Date)
    gender = Column(String(20))
    location = Column(String(100))

    pan_number = Column(String(20))
    pan_card_file = Column(String(255))
    resume_file = Column(String(255)) 
    photo_file = Column(String(255))

    linkedin_url = Column(String(255))

    highest_qualification = Column(String(100))
    specialization = Column(String(100))
    university = Column(String(150))
    college = Column(String(150))
    year_of_passing = Column(Integer)

    position_applied = Column(String(150))
    preferred_work_mode = Column(String(50))
    key_skills = Column(Text)
    expected_salary = Column(Integer)
    why_hire_me = Column(Text)

    experience_level = Column(String(50))
    previous_company = Column(String(150))
    previous_role = Column(String(150))
    date_of_joining = Column(Date)
    relieving_date = Column(Date)

    captcha_verified = Column(Boolean, default=False)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
