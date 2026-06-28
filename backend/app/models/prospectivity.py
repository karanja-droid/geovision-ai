from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ProspectivityTarget(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    score: float
    commodity: str
    confidence: float
    key_features: Dict[str, float] = {}

class PredictRequest(BaseModel):
    project_id: Optional[int] = None
    aoi_geojson: Dict[str, Any]
    commodity: str = "Cu"
    model: str = "demo"
    params: Dict[str, Any] = {}

class PredictResponse(BaseModel):
    run_id: int
    targets: List[ProspectivityTarget]
    summary: str
    map_geojson: Optional[Dict[str, Any]] = None
    confidence_overall: float