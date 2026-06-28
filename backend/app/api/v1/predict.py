from fastapi import APIRouter, Depends
from typing import Dict, Any

from backend.app.models.prospectivity import PredictRequest, PredictResponse
from backend.app.services.prospectivity import run_demo_prospectivity
from backend.app.core.security import get_current_user

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(
    req: PredictRequest,
    user: str = Depends(get_current_user)
):
    """Demo prospectivity inference (Phase 0/2)."""
    result = run_demo_prospectivity(req.aoi_geojson, req.commodity, n_targets=12)
    return result

@router.get("/deposits", response_model=Dict[str, Any])
async def get_demo_deposits():
    """Known occurrences for overlay (Copperbelt demo)."""
    from data.seed.copperbelt_deposits import get_deposits_geojson
    return get_deposits_geojson()

# Phase 1 enhancements: demo data loader + basic spatial query (deposits inside AOI)
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from backend.app.database import get_session
from backend.app.models.core import MineralOccurrence, Project as DBProject
from backend.app.data.seed.copperbelt_deposits import COPPERBELT_DEPOSITS
from shapely import wkt as shapely_wkt
from shapely.geometry import shape as shapely_shape
import json

@router.post("/seed-deposits")
async def seed_demo_deposits(
    user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Phase 1 demo data loader: load Copperbelt known deposits into DB."""
    existing = session.exec(select(MineralOccurrence)).all()
    if len(existing) > 5:
        return {"status": "already_seeded", "count": len(existing)}
    
    for d in COPPERBELT_DEPOSITS:
        occ = MineralOccurrence(
            name=d.name,
            commodity=d.commodity,
            latitude=d.lat,
            longitude=d.lon,
            region=d.region
        )
        occ.geom = f"SRID=4326;POINT({d.lon} {d.lat})"
        session.add(occ)
    session.commit()
    return {"status": "seeded", "count": len(COPPERBELT_DEPOSITS)}

@router.get("/deposits-in-aoi/{project_id}")
async def deposits_in_aoi(
    project_id: int,
    user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Phase 1 basic spatial query example: deposits inside project's AOI (shapely fallback; full ST_Contains in DB later)."""
    proj = session.get(DBProject, project_id)
    if not proj or not proj.aoi_wkt:
        raise HTTPException(status_code=404, detail="Project or AOI not found")
    
    try:
        aoi_poly = shapely_wkt.loads(proj.aoi_wkt)
    except Exception:
        try:
            gj = json.loads(proj.aoi_wkt)
            aoi_poly = shapely_shape(gj["features"][0]["geometry"] if "features" in gj else gj)
        except:
            raise HTTPException(status_code=400, detail="Invalid AOI WKT/GeoJSON")
    
    deposits = session.exec(select(MineralOccurrence)).all()
    inside = []
    for d in deposits:
        if d.geom:
            try:
                pt = shapely_wkt.loads(d.geom.replace("SRID=4326;", ""))
                if pt.within(aoi_poly):
                    inside.append({"id": d.id, "name": d.name, "commodity": d.commodity, "lat": d.latitude, "lon": d.longitude})
            except:
                pass
    
    return {"project_id": project_id, "deposits_inside": inside, "count": len(inside)}