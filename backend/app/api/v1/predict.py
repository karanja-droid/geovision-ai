from fastapi import APIRouter, Depends
from typing import Dict, Any

from backend.app.models.prospectivity import PredictRequest, PredictResponse
from backend.app.services.prospectivity import run_demo_prospectivity
from backend.app.core.security import get_current_user
from data.seed.copperbelt_deposits import get_deposits_geojson

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest, user: str = Depends(get_current_user)):
    return run_demo_prospectivity(req.aoi_geojson, req.commodity)

@router.get("/deposits", response_model=Dict[str, Any])
async def get_demo_deposits():
    return get_deposits_geojson()