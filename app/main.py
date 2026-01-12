from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.database import engine, Base
from app.routes import (
    auth,
    admin_test,
    otp,
    jobs,
    public_jobs,
    job_applications,
    contact,
    csr,
    onboarding_admin,
)

load_dotenv()  # Loads .env file

app = FastAPI(title="VINFAST Backend")

# Root endpoint (for Render health check)
@app.get("/")
def root():
    return {"message": "FastAPI backend running"}

# CORS Configuration (unchanged)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(admin_test.router)
app.include_router(otp.router)
app.include_router(jobs.router)
app.include_router(public_jobs.router)
app.include_router(job_applications.router)
app.include_router(contact.router)
app.include_router(csr.router)
app.include_router(onboarding_admin.router)
