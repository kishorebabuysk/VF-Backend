from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.csr import CSR
from app.schemas.csr import CSRCreate, CSRUpdate, CSRResponse
from app.utils.jwt_dependency import get_current_admin
from app.utils.file_upload import save_upload_file


router = APIRouter( prefix="/csr",tags=["CSR"]
)


@router.get("", response_model=list[CSRResponse])
def list_csr(db: Session = Depends(get_db)):
    """
    Get all active CSR activities (Public)
    """
    return (
        db.query(CSR)
        .filter(CSR.is_active == True)
        .order_by(CSR.created_at.desc())
        .all()
    )


@router.post("/admin/upload")
def upload_csr_image(
    file: UploadFile = File(...),
    admin=Depends(get_current_admin)
):
    """
    Upload CSR image (Admin)
    """
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=400,
            detail="Only JPG or PNG images are allowed"
        )

    file_path = save_upload_file("uploads/csr", file)

    return {
        "file_path": file_path
    }


@router.post("/admin", response_model=CSRResponse)
def create_csr(
    data: CSRCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    Create CSR activity (Admin)
    """
    csr = CSR(**data.dict())
    db.add(csr)
    db.commit()
    db.refresh(csr)
    return csr


@router.put("/admin/{csr_id}", response_model=CSRResponse)
def update_csr(
    csr_id: int,
    data: CSRUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    Update CSR activity (Admin)
    """
    csr = db.query(CSR).filter(CSR.id == csr_id).first()
    if not csr:
        raise HTTPException(status_code=404, detail="CSR not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(csr, key, value)

    db.commit()
    db.refresh(csr)
    return csr


@router.delete("/admin/{csr_id}")
def delete_csr(
    csr_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    Soft delete CSR activity (Admin)
    """
    csr = db.query(CSR).filter(CSR.id == csr_id).first()
    if not csr:
        raise HTTPException(status_code=404, detail="CSR not found")

    csr.is_active = False
    db.commit()

    return {
        "message": "CSR removed successfully"
    }
