from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.csr import CSR
from app.schemas.csr import CSRCreate, CSRUpdate, CSRResponse
from app.utils.jwt_dependency import get_current_admin

router = APIRouter(tags=["CSR"])


# 🔓 PUBLIC – VIEW CSR
@router.get("/csr", response_model=list[CSRResponse])
def list_csr(db: Session = Depends(get_db)):
    return (
        db.query(CSR)
        .filter(CSR.is_active == True)
        .order_by(CSR.created_at.desc())
        .all()
    )


# 🔐 ADMIN – CREATE CSR
@router.post("/admin/csr", response_model=CSRResponse)
def create_csr(
    data: CSRCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    csr = CSR(**data.dict())
    db.add(csr)
    db.commit()
    db.refresh(csr)
    return csr


# 🔐 ADMIN – UPDATE CSR
@router.put("/admin/csr/{csr_id}", response_model=CSRResponse)
def update_csr(
    csr_id: int,
    data: CSRUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    csr = db.query(CSR).filter(CSR.id == csr_id).first()
    if not csr:
        raise HTTPException(status_code=404, detail="CSR not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(csr, key, value)

    db.commit()
    db.refresh(csr)
    return csr


# 🔐 ADMIN – DELETE CSR (SOFT DELETE)
@router.delete("/admin/csr/{csr_id}")
def delete_csr(
    csr_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    csr = db.query(CSR).filter(CSR.id == csr_id).first()
    if not csr:
        raise HTTPException(status_code=404, detail="CSR not found")

    csr.is_active = False
    db.commit()
    return {"message": "CSR removed successfully"}
