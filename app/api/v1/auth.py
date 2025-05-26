from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.deps import get_db, get_current_user
from datetime import timedelta
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.profile import ProfileCreate
from app.crud import user as user_crud
from datetime import datetime, timedelta
from app.core.redis import redis_client

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    expire_seconds = int(access_token_expires.total_seconds())
    redis_client.setex(token, expire_seconds, user.username)

    response = JSONResponse(content={"msg": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=expire_seconds,
        samesite="Strict",
        secure=False,  # True for HTTPS
        path="/",
    )
    return response

@router.post("/register")
def register(user_data: UserCreate, profile_data: ProfileCreate, db: Session = Depends(get_db)):
    # Check if the user already exists.
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    user = user_crud.create_user_with_profile(db, user_data, profile_data)
    return {"message": "User registered successfully", "user_id": user.id}

@router.post("/logout")
def logout(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        expire_duration = exp_timestamp - int(datetime.utcnow().timestamp())

        redis_client.setex(f"blacklisted:{token}", timedelta(seconds=expire_duration), "true")

        response = JSONResponse(content={"msg": "Logout successful"})
        response.delete_cookie("access_token")
        
        return response
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")