# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from app.core.config import settings
from app.api.v1 import auth, users, profile, kyc #, review, results
from app.middleware.token_blacklist import TokenBlacklistMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)


# CORS config
origins = [
    "http://localhost:8000",  # backend local dev
    "http://localhost:5173",  # frontend local dev
]

# COR Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TokenBlacklistMiddleware)

# Create a router with a shared prefix
api_router = APIRouter(prefix="/api/v1")

# Include routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(profile.router)
api_router.include_router(kyc.router)
# api_router.include_router(review.router)
# api_router.include_router(results.router)

# Add the API router to the main app
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "KYC Backend Running!"}