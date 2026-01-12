from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OnboardingNominee(Base):
    __tablename__ = "onboarding_nominees"

    id = Column(Integer, primary_key=True, index=True)
    nominee_type = Column(String(255), nullable=False)  # PF / ESI / Accident
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    dob = Column(Date, nullable=False)
    relationship_type = Column(String(255), nullable=False)
    onboarding_id = Column(Integer, ForeignKey("onboarding.id"))
    onboarding = relationship("Onboarding", back_populates="nominees")


class OnboardingFamily(Base):
    __tablename__ = "onboarding_family"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=False)
    relationship_type = Column(String(255), nullable=False)

    onboarding_id = Column(Integer, ForeignKey("onboarding.id"))
    onboarding = relationship("Onboarding", back_populates="family")


class OnboardingBank(Base):
    __tablename__ = "onboarding_bank"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String(255), nullable=False)
    account_number = Column(String(255), nullable=False)
    ifsc_code = Column(String(255), nullable=False)
    branch_name = Column(String(255), nullable=False)

    onboarding_id = Column(Integer, ForeignKey("onboarding.id"))
    onboarding = relationship("Onboarding", back_populates="bank")


class OnboardingReference(Base):
    __tablename__ = "onboarding_references"

    id = Column(Integer, primary_key=True, index=True)
    reference_type = Column(String(255), nullable=False)  # employee / relative/friend
    name = Column(String(255), nullable=False)
    designation_or_occupation = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    last_employer = Column(String(255), nullable=True)

    onboarding_id = Column(Integer, ForeignKey("onboarding.id"))
    onboarding = relationship("Onboarding", back_populates="references")
