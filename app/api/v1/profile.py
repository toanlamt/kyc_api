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
    profiles = db.query(Profile).all()
    return [
        ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            basicinfo={
                "first_name": profile.first_name,
                "middle_name": profile.middle_name,
                "last_name": profile.last_name,
                "dob": profile.dob,
                "age": profile.age
            },
            addresses=profile.addresses,
            contacts=profile.contacts,
            documents=profile.documents,
            employments=profile.employments,
        )
        for profile in profiles
    ]
@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        basicinfo={
            "first_name": profile.first_name,
            "middle_name": profile.middle_name,
            "last_name": profile.last_name,
            "dob": profile.dob,
            "age": profile.age
        },
        addresses=profile.addresses,
        contacts=profile.contacts,
        documents=profile.documents,
        employments=profile.employments,
    )

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
    return ProfileResponse(
        id=new_profile.id,
        user_id=new_profile.user_id,
        basicinfo={
            "first_name": new_profile.first_name,
            "middle_name": new_profile.middle_name,
            "last_name": new_profile.last_name,
            "dob": new_profile.dob,
        },
        addresses=new_profile.addresses,
        contacts=new_profile.contacts,
        documents=new_profile.documents,
        employments=new_profile.employments,
    )
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
    return ProfileResponse(
        id=updated_profile.id,
        user_id=updated_profile.user_id,
        basicinfo={
            "first_name": updated_profile.first_name,
            "middle_name": updated_profile.middle_name,
            "last_name": updated_profile.last_name,
            "dob": updated_profile.dob,
        },
        addresses=updated_profile.addresses,
        contacts=updated_profile.contacts,
        documents=updated_profile.documents,
        employments=updated_profile.employments,
    )