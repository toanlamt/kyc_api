# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users #, profile, kyc, review, results
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

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(users.router, prefix="/api/v1/users")
# app.include_router(profile.router, prefix="/api/v1/profile")
# app.include_router(kyc.router, prefix="/api/v1/kyc")
# app.include_router(review.router, prefix="/api/v1/review")
# app.include_router(results.router, prefix="/api/v1/results")

@app.get("/")
def root():
    return {"message": "KYC Backend Running!"}