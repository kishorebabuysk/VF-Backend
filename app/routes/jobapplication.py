from fastapi import (
    APIRouter, Depends, HTTPException,
    UploadFile, File, Form, Query, Body
)
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import date
import os

from app.database import get_db
from app.models.jobapplication import Application
from app.schemas.jobapplication import ApplicationCreate, ApplicationResponse
from app.utils.jwt_dependency import get_current_admin
from app.utils.file_upload import save_upload_file
from app.models.admin import Admin as User

router = APIRouter(prefix="/admin/applications", tags=["Job Applications"])

UPLOAD_DIR = "uploads/job_applications"


# -------------------------------------------------------------------
# CREATE APPLICATION
# -------------------------------------------------------------------
@router.post("/", response_model=ApplicationResponse, status_code=201)
async def apply_job(
    job_id: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    date_of_birth: date = Form(...),
    gender: str = Form(...),
    location: str = Form(...),
    pan_number: str = Form(...),
    linkedin_url: Optional[str] = Form(None),

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

    experience_level: str = Form(..., description="fresher | experienced"),

    previous_company: Optional[str] = Form(None),
    previous_role: Optional[str] = Form(None),
    date_of_joining: Optional[date] = Form(None),
    relieving_date: Optional[date] = Form(None),

    captcha_token: str = Form(...),

    pan_card: UploadFile = File(...),
    resume: UploadFile = File(...),
    photo: UploadFile = File(...),

    db: Session = Depends(get_db),
):
    # --------------------------------------------------
    # CAPTCHA CHECK
    # --------------------------------------------------
    if captcha_token != "test":
        raise HTTPException(status_code=400, detail="Invalid CAPTCHA")

    # --------------------------------------------------
    # EXPERIENCE VALIDATION
    # --------------------------------------------------
    if experience_level == "experienced":
        if not all([previous_company, previous_role, date_of_joining, relieving_date]):
            raise HTTPException(
                status_code=422,
                detail="Experienced candidates must provide previous_company, previous_role, date_of_joining, and relieving_date",
            )

    # --------------------------------------------------
    # SCHEMA VALIDATION
    # --------------------------------------------------
    application_create = ApplicationCreate(
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
        job_id=job_id,
    )

    # --------------------------------------------------
    # FILE UPLOADS (UTILITY FUNCTION)
    # --------------------------------------------------
    pan_card_path = save_upload_file(UPLOAD_DIR, pan_card)
    resume_path = save_upload_file(UPLOAD_DIR, resume)
    photo_path = save_upload_file(UPLOAD_DIR, photo)

    # --------------------------------------------------
    # DATABASE SAVE
    # --------------------------------------------------
    db_application = Application(
        **application_create.dict(),
        pan_card_file=pan_card_path,
        resume_file=resume_path,
        photo_file=photo_path,
        status="Pending",
        captcha_verified=True,
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application

# -------------------------------------------------------------------
# GET ALL APPLICATIONS
# -------------------------------------------------------------------
@router.get("/getall", response_model=List[ApplicationResponse])
async def get_all_applications(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    current_user: User = Depends(get_current_admin),
):
    applications = db.query(Application).offset(skip).limit(limit).all()
    return applications

# -------------------------------------------------------------------
# LIST APPLICATIONS
# -------------------------------------------------------------------
@router.get("/", response_model=dict)
async def list_applications(
    job_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    query = db.query(Application)

    if job_id:
        query = query.filter(Application.job_id == job_id)
    if status:
        query = query.filter(Application.status == status)

    applications = query.all()

    stats_query = db.query(Application.status, func.count(Application.id))
    if job_id:
        stats_query = stats_query.filter(Application.job_id == job_id)
    stats_query = stats_query.group_by(Application.status)

    status_counts = dict(stats_query.all())

    return {
        "applications": [ApplicationResponse.model_validate(a) for a in applications],
        "stats": {
            "total": len(applications),
            "pending": status_counts.get("pending", 0),
            "shortlisted": status_counts.get("shortlisted", 0),
            "maybe": status_counts.get("maybe", 0),
            "rejected": status_counts.get("rejected", 0),
            "by_status": status_counts,
        },
    }


# -------------------------------------------------------------------
# GET SINGLE APPLICATION
# -------------------------------------------------------------------
@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


# -------------------------------------------------------------------
# UPDATE STATUS
# -------------------------------------------------------------------
@router.patch("/{application_id}/status")
async def update_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    old_status = application.status
    application.status = status

    db.commit()
    db.refresh(application)

    return {
        "id": application.id,
        "old_status": old_status,
        "new_status": status,
        "message": "Status updated successfully",
    }


# -------------------------------------------------------------------
# DELETE SINGLE APPLICATION
# -------------------------------------------------------------------
@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    for field in ["pan_card_file", "resume_file", "photo_file"]:
        file_path = getattr(application, field)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    db.delete(application)
    db.commit()

    return {"message": "Application deleted successfully"}


# -------------------------------------------------------------------
# BULK DELETE
# -------------------------------------------------------------------
@router.delete("/bulk")
async def delete_applications_bulk(
    application_ids: List[int] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    deleted = 0

    for app_id in application_ids:
        app = db.query(Application).filter(Application.id == app_id).first()
        if app:
            for field in ["pan_card_file", "resume_file", "photo_file"]:
                file_path = getattr(app, field)
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)

            db.delete(app)
            deleted += 1

    db.commit()
    return {"message": f"Deleted {deleted} applications"}
