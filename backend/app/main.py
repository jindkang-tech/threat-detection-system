from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from .api.endpoints import threats, alerts, models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Threat Detection System",
    description="Real-time threat detection and response system using AI/ML",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(threats.router, prefix="/api/v1/threats", tags=["threats"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])

@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.VERSION,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up AI-Driven Threat Detection System...")
    # Initialize any required services or connections here

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down AI-Driven Threat Detection System...")
    # Clean up any resources here
