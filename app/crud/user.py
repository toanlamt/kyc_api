from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.models.kyc import KYC
from app.schemas.user import UserCreate
from app.schemas.profile import ProfileBase
from app.core.security import hash_password

def create_user_with_profile(db: Session, user_data: UserCreate, profile_data: ProfileBase):
    user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(user)
    db.flush() # Create the user first to get the user ID.

    profile = Profile(
        user_id=user.id,
        first_name=profile_data.first_name,
        middle_name=profile_data.middle_name,
        last_name=profile_data.last_name,
        dob=profile_data.dob,
        age=profile_data.age
    )
    db.add(profile)

    kyc = KYC(
        user_id=user.id,
    )
    db.add(kyc)

    db.commit()
    db.refresh(user)
    return user
