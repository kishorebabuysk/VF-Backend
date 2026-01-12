from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.job import Job
from app.models.job_application import JobApplication
from app.schemas.job_application import JobApplicationDetailResponse,BulkDeleteRequest
from app.utils.resume_upload import save_resume
from app.utils.jwt_dependency import get_current_admin
from fastapi import UploadFile
import os
from app.utils.file_upload import save_file


router = APIRouter(
    prefix="/admin/applications",   
    tags=["Job Applications"]
    
)

UPLOAD_DIR = "uploads/job_applications"
os.makedirs(UPLOAD_DIR, exist_ok=True)


'''
@router.post("/")
def apply_job(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    date_of_birth: str = Form(...),
    gender: str = Form(...),
    location: str = Form(...),

    pan_number: str = Form(...),
    linkedin_url: str = Form(None),

    highest_qualification: str = Form(...),
    specialization: str = Form(...),
    university: str = Form(...),
    college: str = Form(...),
    year_of_passing: int = Form(...),

    position_applied: str = Form(...),
    preferred_work_mode: str = Form(...),
    key_skills: str = Form(...),
    expected_salary: int = Form(...),
    why_hire_me: str = Form(...),

    experience_level: str = Form(...),

    previous_company: str = Form(None),
    previous_role: str = Form(None),
    date_of_joining: str = Form(None),
    relieving_date: str = Form(None),

    captcha_verified: bool = Form(...),

    pan_card: UploadFile = File(...),
    resume: UploadFile = File(...),
    photo: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    if not captcha_verified:
        raise HTTPException(status_code=400, detail="Captcha not verified")
    
    def save_file(file: UploadFile):
        path = f"{UPLOAD_DIR}/{file.filename}"
        with open(path, "wb") as f:
            f.write(file.file.read())
        return path

    application = JobApplication(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        date_of_birth=date_of_birth,
        gender=gender,
        location=location,
        pan_number=pan_number,
        linkedin_url=linkedin_url,

        highest_qualification=highest_qualification,
        specialization=specialization,
        university=university,
        college=college,
        year_of_passing=year_of_passing,

        position_applied=position_applied,
        preferred_work_mode=preferred_work_mode,
        key_skills=key_skills,
        expected_salary=expected_salary,
        why_hire_me=why_hire_me,

        experience_level=experience_level,

        previous_company=previous_company,
        previous_role=previous_role,
        date_of_joining=date_of_joining,
        relieving_date=relieving_date,

        pan_card_file=save_file(pan_card),
        resume_file=save_file(resume),
        photo_file=save_file(photo),

        captcha_verified=captcha_verified
    )

    db.add(application)
    db.commit()
    return {"message": "Job application submitted successfully"}'''

@router.post("/")
def apply_job(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    date_of_birth: str = Form(...),
    gender: str = Form(...),
    location: str = Form(...),

    pan_number: str = Form(...),
    linkedin_url: str = Form(None),

    highest_qualification: str = Form(...),
    specialization: str = Form(...),
    university: str = Form(...),
    college: str = Form(...),
    year_of_passing: int = Form(...),

    position_applied: str = Form(...),
    preferred_work_mode: str = Form(...),
    key_skills: str = Form(...),
    expected_salary: int = Form(...),
    why_hire_me: str = Form(...),

    experience_level: str = Form(...),

    previous_company: str = Form(None),
    previous_role: str = Form(None),
    date_of_joining: str = Form(None),
    relieving_date: str = Form(None),

    captcha_verified: bool = Form(...),

    pan_card: UploadFile = File(...),
    resume: UploadFile = File(...),
    photo: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    if not captcha_verified:
        raise HTTPException(status_code=400, detail="Captcha not verified")

    try:
        pan_card_path = save_file(pan_card)
        resume_path = save_file(resume)
        photo_path = save_file(photo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File upload failed: {str(e)}")

    try:
        full_name = f"{first_name} {last_name}".strip()
        application = JobApplication(
            full_name=full_name,   

            phone=phone,
            email=email,
            date_of_birth=date_of_birth,
            gender=gender,
            location=location,

            pan_number=pan_number,
            linkedin_url=linkedin_url,

            highest_qualification=highest_qualification,
            specialization=specialization,
            university=university,
            college=college,
            year_of_passing=year_of_passing,

            position_applied=position_applied,
            preferred_work_mode=preferred_work_mode,
            key_skills=key_skills,
            expected_salary=expected_salary,
            why_hire_me=why_hire_me,

            experience_level=experience_level,

            previous_company=previous_company,
            previous_role=previous_role,
            date_of_joining=date_of_joining,
            relieving_date=relieving_date,

            pan_card_file=pan_card_path,
            resume_file=resume_path,
            photo_file=photo_path,

            captcha_verified=captcha_verified
        )

        db.add(application)
        db.commit()
        db.refresh(application)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "message": "Job application submitted successfully",
        "application_id": application.id
    }

@router.get(
    "/job-applications",
    response_model=list[JobApplicationDetailResponse]
)
def list_job_applications(db: Session = Depends(get_db)):
    return (
        db.query(JobApplication)
        .order_by(JobApplication.created_at.desc())
        .all()
    )







@router.get("/{application_id}", response_model=JobApplicationDetailResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application





@router.delete("/{application_id}")
def hard_delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    application = (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()

    return {"message": "Job application permanently deleted"}

@router.post("/bulk-delete")
def bulk_hard_delete_applications(
    payload: BulkDeleteRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    applications = (
        db.query(JobApplication)
        .filter(JobApplication.id.in_(payload.application_ids))
        .all()
    )

    if not applications:
        raise HTTPException(status_code=404, detail="No applications found")

    for app in applications:
        db.delete(app)

    db.commit()

    return {
        "message": f"{len(applications)} applications permanently deleted"
    }