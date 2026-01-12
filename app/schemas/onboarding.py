from pydantic import BaseModel, EmailStr, field_validator, model_validator
from datetime import date
from typing import List, Optional

# -------- Documents --------
class DocumentCreate(BaseModel):
    document_type: str
    file_path: str

class DocumentResponse(DocumentCreate):
    class Config:
        from_attributes = True

# -------- Nominee --------
class NomineeCreate(BaseModel):
    nominee_type: str  # PF / ESI / Accident
    name: str
    age: Optional[int] = None
    dob: date
    relationship_type: str

class NomineeResponse(NomineeCreate):
    class Config:
        from_attributes = True

# -------- Family --------
class FamilyCreate(BaseModel):
    name: str
    dob: date
    relationship_type: str

class FamilyResponse(FamilyCreate):
    class Config:
        from_attributes = True

# -------- Bank --------
class BankCreate(BaseModel):
    account_name: str
    account_number: str
    ifsc_code: str
    branch_name: str

class BankResponse(BankCreate):
    class Config:
        from_attributes = True

# -------- References --------
class ReferenceCreate(BaseModel):
    reference_type: str  # employee / relative_friend
    name: str
    designation_or_occupation: Optional[str] = None
    phone: str
    email: Optional[str] = None
    last_employer: Optional[str] = None

class ReferenceResponse(ReferenceCreate):
    class Config:
        from_attributes = True

# -------- Checklist --------
class ChecklistCreate(BaseModel):
    experience_type: str  # fresher / experienced
    aadhar_card: bool = False
    pan_card: bool = False
    qualification_certificates: bool = False
    passport_size: bool = False
    bank_account: bool = False
    employer_reference_check: bool = False

    relieving_letter: Optional[bool] = False
    pay_slips: Optional[bool] = False
    offer_letter: Optional[bool] = False
    hike_letter: Optional[bool] = False
    experience_letter: Optional[bool] = False

class ChecklistResponse(ChecklistCreate):
    class Config:
        from_attributes = True

# -------- Main Onboarding --------
class OnboardingCreate(BaseModel):
    # Personal Info
    name: str
    dob: date
    marital_status: Optional[str] = None
    gender: str
    aadhar_number: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    spouse_name: Optional[str] = None
    communication_address: str
    permanent_address: str
    landline_number: Optional[str] = None
    mobile_number: str
    email: EmailStr
    blood_group: Optional[str] = None
    emergency_contact1: str
    emergency_contact2: Optional[str] = None
    education_qualification: Optional[str] = None
    driving_license: Optional[str] = None
    vehicle_number: Optional[str] = None
    applied_role: str
    experience_type: str  # fresher / experienced

    # Experienced-only
    company_name: Optional[str] = None
    job_role: Optional[str] = None
    date_of_joining: Optional[date] = None
    date_of_exit: Optional[date] = None
    total_experience: Optional[str] = None
    esi_number: Optional[str] = None
    uan_number: Optional[str] = None

    # Nested
    documents: List[DocumentCreate]
    nominees: List[NomineeCreate]
    family: List[FamilyCreate]
    bank: BankCreate
    references: List[ReferenceCreate]
    checklist: ChecklistCreate

    @model_validator(mode="after")
    def validate_experienced_fields(cls, values):
        if values.experience_type.lower() == "experienced":
            required = ["company_name", "job_role", "date_of_joining", "date_of_exit", "total_experience"]
            missing = [f for f in required if not getattr(values, f)]
            if missing:
                raise ValueError(f"Missing required fields for experienced candidate: {missing}")
        return values

class OnboardingResponse(BaseModel):
    id: int
    name: str
    dob: date
    marital_status: Optional[str]
    gender: str
    aadhar_number: str
    father_name: Optional[str]
    mother_name: Optional[str]
    spouse_name: Optional[str]
    communication_address: str
    permanent_address: str
    landline_number: Optional[str]
    mobile_number: str
    email: str
    blood_group: Optional[str]
    emergency_contact1: str
    emergency_contact2: Optional[str]
    education_qualification: Optional[str]
    driving_license: Optional[str]
    vehicle_number: Optional[str]
    applied_role: str
    experience_type: str

    company_name: Optional[str]
    job_role: Optional[str]
    date_of_joining: Optional[date]
    date_of_exit: Optional[date]
    total_experience: Optional[str]
    esi_number: Optional[str]
    uan_number: Optional[str]

    status: str

    documents: List[DocumentResponse] = []
    nominees: List[NomineeResponse] = []
    family: List[FamilyResponse] = []
    references: List[ReferenceResponse] = []
    bank: Optional[BankResponse] = None
    checklist: Optional[ChecklistResponse] = None

    class Config:
        from_attributes = True
