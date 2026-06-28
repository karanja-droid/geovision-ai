"""
GeoVision AI Backend — FastAPI application (Phase 0 foundation per DEVELOPMENT_LOOP.md)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.app.core.config import settings
from backend.app.core.security import get_current_user  # used in routers

# Routers
from backend.app.api.v1.projects import router as projects_router
from backend.app.api.v1.predict import router as predict_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geovision")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting GeoVision AI backend (Phase 0 + Phase 1 data layer enhancements)")
    # For demo/Phase 1: create tables if not using full migrations yet.
    # In production use Alembic. PostGIS extension should be enabled in the DB (docker compose does it).
    from backend.app.database import engine
    from backend.app.models.core import SQLModel
    # Import all models so metadata is populated for create_all
    from backend.app.models import core, prospectivity  # noqa: F401
    SQLModel.metadata.create_all(bind=engine)
    logger.info("✅ DB tables ensured")
    yield
    logger.info("🛑 Shutting down GeoVision AI backend")

app = FastAPI(
    title=settings.app_name,
    description="AI geospatial mineral prospectivity for Southern Africa. See docs/DEVELOPMENT_LOOP.md",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS (permissive for MVP demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"])
async def health():
    """Liveness / readiness probe."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "phase": "0-foundation + phase1-data"
    }

@app.get("/", tags=["system"])
async def root():
    return {
        "message": "Welcome to GeoVision AI (Phase 0+1). See /docs and docs/DEVELOPMENT_LOOP.md",
        "docs": "/docs",
        "health": "/health"
    }

# Include routers
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(predict_router, prefix="/api/v1", tags=["predict"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
