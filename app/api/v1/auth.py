from fastapi import APIRouter, Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.deps import get_db, get_current_user
from datetime import timedelta
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.schemas.profile import ProfileCreate
from app.crud import user as user_crud
from datetime import datetime, timedelta
from app.core.redis import redis_client

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    expire = int(access_token_expires.total_seconds())
    redis_client.setex(token, expire, user.username)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserCreate, profile_data: ProfileCreate, db: Session = Depends(get_db)):
    # Check if the user already exists.
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    user = user_crud.create_user_with_profile(db, user_data, profile_data)
    return {"message": "User registered successfully", "user_id": user.id}

@router.post("/logout")
def logout(request: Request,  current_user: User = Depends(get_current_user)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        expire_duration = exp_timestamp - int(datetime.utcnow().timestamp())

        redis_client.setex(f"blacklisted:{token}", timedelta(seconds=expire_duration), "true")

        return {"msg": "Logout successful"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")