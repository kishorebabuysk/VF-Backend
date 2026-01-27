from sqlalchemy import Column, Integer, String, Float, Text, Date, DateTime, func
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    jobTitle = Column(String(255), nullable=False)
    department = Column(String(50), nullable=False)
    workMode = Column(String(50), nullable=False)
    rolesResponsibilities = Column(Text, nullable=False)
    requiredSkills = Column(Text, nullable=False)
    experienceMin = Column(Float, nullable=False)
    experienceMax = Column(Float, nullable=False)
    qualification = Column(String(255), nullable=False)
    salaryMin = Column(Float, nullable=False)
    salaryMax = Column(Float, nullable=False)
    perksBenefits = Column(Text, nullable=True)
    jobLocation = Column(String(255), nullable=False)
    jobLocality = Column(String(255), nullable=True)
    numOpenings = Column(Integer, nullable=False)
    applicationDeadline = Column(Date, nullable=False)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)