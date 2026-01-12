from fastapi import APIRouter, Depends, HTTPException,File,UploadFile,Query
from sqlalchemy.orm import Session
from sqlalchemy import or_


from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobResponse,PaginatedJobResponse
from app.utils.jwt_dependency import get_current_admin



router = APIRouter(prefix="/admin/jobs", tags=["Admin Jobs"])

@router.post("/admin/jobs/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    new_job = Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job



@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in job.dict(exclude_unset=True).items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)
    return db_job




@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

@router.delete("/bulk-delete/")
def bulk_delete_jobs(
    job_ids: list[int] = Query(..., description="List of Job IDs to delete"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found for the provided IDs")

    for job in jobs:
        db.delete(job)
    db.commit()
    return {"message": f"Deleted {len(jobs)} jobs successfully"}


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/jobs/", response_model=list[JobResponse])
def admin_list_jobs(
    q: str | None = Query(None, description="Search keyword"),
    department: str | None = None,
    location: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    query = db.query(Job)

    # 🔍 Search
    if q:
        query = query.filter(
            or_(
                Job.title.ilike(f"%{q}%"),
                Job.description.ilike(f"%{q}%")
            )
        )

    # 🎯 Filters
    if department:
        query = query.filter(Job.department == department)
    if location:
        query = query.filter(Job.location == location)

    # 📄 Pagination
    offset = (page - 1) * limit
    jobs = (
        query
        .order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return jobs



@router.delete("/{job_id}", summary=" Delete job ")
def hard_delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return {"message": "Job permanently deleted"}






