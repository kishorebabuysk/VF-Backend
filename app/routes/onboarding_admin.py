from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session, joinedload
from typing import List
import os, shutil, uuid

from app.database import get_db
from app.schemas.onboarding import OnboardingCreate, OnboardingResponse
from app.models.onboarding import Onboarding
from app.models.onboarding_documents import OnboardingDocument
from app.models.onboarding_nominee import OnboardingNominee, OnboardingFamily, OnboardingBank, OnboardingReference
from app.models.onboarding_checklist import OnboardingChecklist
from app.utils.jwt_dependency import get_current_admin

UPLOAD_DIR = "uploads/onboarding"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/admin/onboarding", tags=["Onboarding"])

@router.get("/admin/onboarding")
def admin_onboarding(current_admin=Depends(get_current_admin)):
    return {"message": "Admin authenticated", "admin": current_admin}

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    safe_name = os.path.basename(file.filename)
    filename = f"{uuid.uuid4()}_{safe_name}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": path}

@router.post("/", response_model=OnboardingResponse)
def create_onboarding(
    data: OnboardingCreate,
    db: Session = Depends(get_db)
):
    try:
        # 🔐 CHECK: One onboarding per user (email-based)
        existing = (
            db.query(Onboarding)
            .filter(Onboarding.email == data.email)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Onboarding already submitted for this user"
            )

        onboarding = Onboarding(
            name=data.name,
            dob=data.dob,
            marital_status=data.marital_status,
            gender=data.gender,
            aadhar_number=data.aadhar_number,
            father_name=data.father_name,
            mother_name=data.mother_name,
            spouse_name=data.spouse_name,
            communication_address=data.communication_address,
            permanent_address=data.permanent_address,
            landline_number=data.landline_number,
            mobile_number=data.mobile_number,
            email=data.email,
            blood_group=data.blood_group,
            emergency_contact1=data.emergency_contact1,
            emergency_contact2=data.emergency_contact2,
            education_qualification=data.education_qualification,
            driving_license=data.driving_license,
            vehicle_number=data.vehicle_number,
            applied_role=data.applied_role,
            experience_type=data.experience_type,
            company_name=data.company_name,
            job_role=data.job_role,
            date_of_joining=data.date_of_joining,
            date_of_exit=data.date_of_exit,
            total_experience=data.total_experience,
            esi_number=data.esi_number,
            uan_number=data.uan_number,
            status="pending",
        )

        db.add(onboarding)
        db.flush()

        # ================= DOCUMENTS =================
        if data.documents:
            for doc in data.documents:
                onboarding.documents.append(
                    OnboardingDocument(
                        document_type=doc.document_type,
                        file_path=doc.file_path,
                        onboarding_id=onboarding.id
                    )
                )

        # ================= NOMINEES =================
        if data.nominees:
            for nominee in data.nominees:
                onboarding.nominees.append(
                    OnboardingNominee(
                        nominee_type=nominee.nominee_type,
                        name=nominee.name,
                        age=nominee.age,
                        dob=nominee.dob,
                        relationship_type=nominee.relationship_type,
                        onboarding_id=onboarding.id
                    )
                )

        # ================= FAMILY =================
        if data.family:
            for member in data.family:
                onboarding.family.append(
                    OnboardingFamily(
                        name=member.name,
                        dob=member.dob,
                        relationship_type=member.relationship_type,
                        onboarding_id=onboarding.id
                    )
                )

        # ================= BANK =================
        if data.bank:
            onboarding.bank = OnboardingBank(
                account_name=data.bank.account_name,
                account_number=data.bank.account_number,
                ifsc_code=data.bank.ifsc_code,
                branch_name=data.bank.branch_name,
                onboarding_id=onboarding.id
            )

        # ================= REFERENCES =================
        if data.references:
            for ref in data.references:
                onboarding.references.append(
                    OnboardingReference(
                        reference_type=ref.reference_type,
                        name=ref.name,
                        designation_or_occupation=ref.designation_or_occupation,
                        phone=ref.phone,
                        email=ref.email,
                        last_employer=ref.last_employer,
                        onboarding_id=onboarding.id
                    )
                )

        # ================= CHECKLIST =================
        if data.checklist:
            onboarding.checklist = OnboardingChecklist(
                experience_type=data.checklist.experience_type,
                aadhar_card=data.checklist.aadhar_card,
                pan_card=data.checklist.pan_card,
                qualification_certificates=data.checklist.qualification_certificates,
                passport_size=data.checklist.passport_size,
                bank_account=data.checklist.bank_account,
                employer_reference_check=data.checklist.employer_reference_check,
                relieving_letter=data.checklist.relieving_letter or False,
                pay_slips=data.checklist.pay_slips or False,
                offer_letter=data.checklist.offer_letter or False,
                hike_letter=data.checklist.hike_letter or False,
                experience_letter=data.checklist.experience_letter or False,
                onboarding_id=onboarding.id
            )

        db.commit()
        db.refresh(onboarding)
        return onboarding

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/", response_model=List[OnboardingResponse])
def list_onboardings(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    onboardings = (
        db.query(Onboarding)
        .options(
            joinedload(Onboarding.documents),
            joinedload(Onboarding.nominees),
            joinedload(Onboarding.family),
            joinedload(Onboarding.bank),
            joinedload(Onboarding.references),
            joinedload(Onboarding.checklist),
        )
        .all()
    )
    return onboardings


@router.get("/{onboarding_id}", response_model=OnboardingResponse)
def get_onboarding_by_id(
    onboarding_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    onboarding = (
        db.query(Onboarding)
        .options(
            joinedload(Onboarding.documents),
            joinedload(Onboarding.nominees),
            joinedload(Onboarding.family),
            joinedload(Onboarding.bank),
            joinedload(Onboarding.references),
            joinedload(Onboarding.checklist),
        )
        .filter(Onboarding.id == onboarding_id)
        .first()
    )
    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")
    return onboarding


@router.delete("/{onboarding_id}")
def delete_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()
    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")

    db.delete(onboarding)
    db.commit()
    return {
        "message": "Onboarding deleted permanently",
        "onboarding_id": onboarding_id
    }


@router.delete("/bulk-delete/")
def bulk_delete_onboardings(
    onboarding_ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    onboardings = db.query(Onboarding).filter(Onboarding.id.in_(onboarding_ids)).all()
    if not onboardings:
        raise HTTPException(
            status_code=404,
            detail="No onboardings found for the provided IDs"
        )

    for onboarding in onboardings:
        db.delete(onboarding)

    db.commit()
    return {
        "message": f"Deleted {len(onboardings)} onboardings successfully"
    }
