from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.kyc import KYC
from app.schemas.kyc import KYC as KYCSchema, KYCCreate, KYCUpdate
from app.crud.kyc import update_kyc
from app.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/kyc", tags=["KYC"])

@router.get("/", response_model=List[KYCSchema])
async def get_all_kyc(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "officer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only officers can access all KYC data")
    
    kyc_records = db.query(KYC).all()
    return kyc_records

@router.get("/{user_id}", response_model=KYCSchema)
async def get_kyc_by_user_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "user" and user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="KYC record not found")
     
    kyc = db.query(KYC).filter(KYC.user_id == user_id).first()
    if not kyc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KYC record not found")
    return kyc

@router.put("/", response_model=KYCSchema)
async def update_kyc_endpoint(
    data: KYCUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only normal users can update profile")
    
    kyc = db.query(KYC).filter(data.user_id == current_user.id).first()
    print(kyc)
    if not kyc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KYC record not found")
    
    updated_kyc = update_kyc(db, kyc.id, data)
    return updated_kyc