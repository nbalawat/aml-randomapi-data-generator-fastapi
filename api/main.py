"""
FastAPI application for AML investigation.
"""
import os
import sys

# Add the parent directory to Python path to make imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .aml_routes import router as aml_router

app = FastAPI(
    title="AML Analysis API",
    description="API for Anti-Money Laundering analysis and data retrieval",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(aml_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to AML Analysis API"}
