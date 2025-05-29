from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.address import Address
from app.models.contact import Contact
from app.models.document import Document
from app.models.employment import Employment
from app.schemas.profile import ProfileCreate

def create_profile(db: Session, user_id: int, profile_data: ProfileCreate):
    new_profile = Profile(user_id=user_id, **profile_data.dict(exclude={"addresses", "contacts", "documents", "employments"}))
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

def update_profile(db: Session, user_id: int, profile_data: ProfileCreate):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if profile:
        # Update main profile fields.
        for key, value in profile_data.dict(exclude={"addresses", "contacts", "documents", "employments"}).items():
            setattr(profile, key, value)

    
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