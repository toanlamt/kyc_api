from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.schemas.profile import ProfileResponse, ProfileCreate
from app.models.profile import Profile
from app.crud.profile import create_profile, update_profile
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/profile", tags=["Users Profile"])


@router.get("/", response_model=List[ProfileResponse])
async def get_all_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(Profile).all()
    return users

@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile

@router.post("/", response_model=ProfileResponse)
def create_profile_endpoint(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists.")
    
    new_profile = create_profile(db, current_user.id, data)
    return new_profile

@router.put("/", response_model=ProfileResponse)
async def update_profile_endpoint(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only normal users can update profile")

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    updated_profile = update_profile(db, current_user.id, data)
    return updated_profile