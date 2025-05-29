from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.schemas.profile import ProfileResponse, ProfileCreate
from app.models.profile import Profile
from app.models.address import Address
from app.models.contact import Contact
from app.models.document import Document
from app.models.employment import Employment
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
def create_profile(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists.")
    
    new_profile = Profile(user_id=current_user.id, **data.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.put("/", response_model=ProfileResponse)
async def get_user_by_id(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only normal users can update profile")

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    profile.first_name = data.first_name
    profile.middle_name = data.middle_name
    profile.last_name = data.last_name
    profile.dob = data.dob
    profile.age = data.age

    # Delete old data.
    db.query(Address).filter_by(profile_id=profile.id).delete()
    db.query(Contact).filter_by(profile_id=profile.id).delete()
    db.query(Document).filter_by(profile_id=profile.id).delete()
    db.query(Employment).filter_by(profile_id=profile.id).delete()

    # Add new sub-data.
    for address in data.addresses:
        db.add(Address(profile_id=profile.id, **address.dict()))
    for contact in data.contacts:
        db.add(Contact(profile_id=profile.id, **contact.dict()))
    for document in data.documents:
        db.add(Document(profile_id=profile.id, **document.dict()))
    for employment in data.employments:
        db.add(Employment(profile_id=profile.id, **employment.dict()))

    db.commit()
    db.refresh(profile)
    return profile