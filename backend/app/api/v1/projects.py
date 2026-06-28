from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import BaseModel

from backend.app.core.security import get_current_user
from backend.app.database import get_session
from backend.app.models.core import Project as DBProject
from backend.app.data.seed.copperbelt_deposits import COPPERBELT_DEPOSITS

router = APIRouter()

class ProjectIn(BaseModel):
    name: str
    country: str = "Zambia"
    commodity: str = "Cu"
    description: Optional[str] = None
    aoi_wkt: Optional[str] = None

class ProjectOut(ProjectIn):
    id: int
    analyses_count: int = 0

@router.post("", response_model=ProjectOut)
async def create_project(
    p: ProjectIn, 
    user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_proj = DBProject(**p.model_dump())
    session.add(db_proj)
    session.commit()
    session.refresh(db_proj)
    return ProjectOut(
        id=db_proj.id,
        name=db_proj.name,
        country=db_proj.country,
        commodity=db_proj.commodity,
        description=db_proj.description,
        aoi_wkt=db_proj.aoi_wkt,
        analyses_count=db_proj.analyses_count or 0
    )

@router.get("", response_model=List[ProjectOut])
async def list_projects(
    user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    projects = session.exec(select(DBProject)).all()
    if not projects:
        # Seed a demo project for Phase 1
        demo = DBProject(
            name="Copperbelt Demo Project",
            country="Zambia",
            commodity="Cu",
            description="Pre-loaded for quick start (Phase 1 data layer demo)",
            aoi_wkt="POLYGON((27.6 -12.3, 28.1 -12.3, 28.1 -12.7, 27.6 -12.7, 27.6 -12.3))",
            analyses_count=1
        )
        session.add(demo)
        session.commit()
        session.refresh(demo)
        projects = [demo]
    return [
        ProjectOut(
            id=p.id,
            name=p.name,
            country=p.country,
            commodity=p.commodity,
            description=p.description,
            aoi_wkt=p.aoi_wkt,
            analyses_count=p.analyses_count or 0
        ) for p in projects
    ]

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: int, 
    user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    p = session.get(DBProject, project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectOut(
        id=p.id,
        name=p.name,
        country=p.country,
        commodity=p.commodity,
        description=p.description,
        aoi_wkt=p.aoi_wkt,
        analyses_count=p.analyses_count or 0
    )

@router.post("/{project_id}/aoi", response_model=ProjectOut)
async def set_aoi(
    project_id: int,
    aoi: dict,  # expects {"wkt": "..."} or {"geojson": {...}}
    user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Phase 1 ingestion: set AOI via WKT or GeoJSON for a project."""
    p = session.get(DBProject, project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project or AOI not found")
    
    if "wkt" in aoi:
        p.aoi_wkt = aoi["wkt"]
    elif "geojson" in aoi:
        # For simplicity, store as text (full geom parsing in later)
        p.aoi_wkt = str(aoi["geojson"])
    else:
        raise HTTPException(status_code=400, detail="Provide 'wkt' or 'geojson'")
    
    session.add(p)
    session.commit()
    session.refresh(p)
    return ProjectOut(
        id=p.id, name=p.name, country=p.country, commodity=p.commodity,
        description=p.description, aoi_wkt=p.aoi_wkt, analyses_count=p.analyses_count or 0
    )