from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.address import Address
from app.models.contact import Contact
from app.models.document import Document
from app.models.employment import Employment
from app.schemas.profile import ProfileCreate, ProfileUpdate

def create_profile(db: Session, user_id: int, profile_data: ProfileCreate):
    new_profile = Profile(
        user_id=user_id,
        first_name=profile_data.basicinfo.first_name,
        middle_name=profile_data.basicinfo.middle_name,
        last_name=profile_data.basicinfo.last_name,
        dob=profile_data.basicinfo.dob,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    for address in profile_data.addresses:
        db.add(Address(profile_id=new_profile.id, **address.dict()))
    for contact in profile_data.contacts:
        db.add(Contact(profile_id=new_profile.id, **contact.dict()))
    for document in profile_data.documents:
        db.add(Document(profile_id=new_profile.id, **document.dict()))
    for employment in profile_data.employments:
        db.add(Employment(profile_id=new_profile.id, **employment.dict()))

    db.commit()
    return new_profile

def update_profile(db: Session, user_id: int, profile_data: ProfileUpdate):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if profile:
        # Update fields
        if profile_data.basicinfo.first_name:
            profile.first_name = profile_data.basicinfo.first_name
        if profile_data.basicinfo.middle_name is not None:
            profile.middle_name = profile_data.basicinfo.middle_name
        if profile_data.basicinfo.last_name:
            profile.last_name = profile_data.basicinfo.last_name
        if profile_data.basicinfo.dob:
            profile.dob = profile_data.basicinfo.dob    

    
        db.query(Address).filter_by(profile_id=profile.id).delete()
        db.query(Contact).filter_by(profile_id=profile.id).delete()
        db.query(Document).filter_by(profile_id=profile.id).delete()
        db.query(Employment).filter_by(profile_id=profile.id).delete()

        for address in profile_data.addresses:
            db.add(Address(profile_id=profile.id, **address.dict()))
        for contact in profile_data.contacts:
            db.add(Contact(profile_id=profile.id, **contact.dict()))
        for document in profile_data.documents:
            db.add(Document(profile_id=profile.id, **document.dict()))
        for employment in profile_data.employments:
            db.add(Employment(profile_id=profile.id, **employment.dict()))

        db.commit()
        db.refresh(profile)
        return profile