from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from sqlalchemy import or_


from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse
from app.schemas.job import PaginatedJobResponse


router = APIRouter(prefix="/jobs", tags=["Public Jobs"])




@router.get("/", response_model=PaginatedJobResponse)
def list_jobs(
    q: str | None = Query(None),
    department: str | None = None,
    location: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Job).filter(Job.is_active == True)

    if q:
        query = query.filter(
            or_(
                Job.title.ilike(f"%{q}%"),
                Job.description.ilike(f"%{q}%"),
                Job.department.ilike(f"%{q}%"),
                Job.location.ilike(f"%{q}%")
            )
        )

    if department:
        query = query.filter(Job.department == department)
    if location:
        query = query.filter(Job.location == location)

    total = query.count()

    offset = (page - 1) * limit
    jobs = (
        query
        .order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": jobs
    }

@router.get("/{job_id}", response_model=JobResponse)
def job_detail(job_id: int, db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.id == job_id, Job.is_active == True).first()

