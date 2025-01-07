"""
FastAPI application for AML investigation.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .aml_routes import router as aml_router

# Create FastAPI app
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

# Include the AML routes
app.include_router(aml_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the AML Analysis API"}

