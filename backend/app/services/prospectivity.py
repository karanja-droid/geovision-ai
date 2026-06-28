from typing import List, Dict, Any
import math
from data.seed.copperbelt_deposits import COPPERBELT_DEPOSITS, get_deposits_geojson
from backend.app.models.prospectivity import ProspectivityTarget, PredictResponse

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def run_demo_prospectivity(aoi_geojson: Dict[str, Any], commodity: str = "Cu", n_targets: int = 12) -> PredictResponse:
    coords = aoi_geojson["features"][0]["geometry"]["coordinates"][0]
    center_lon = sum(p[0] for p in coords) / len(coords)
    center_lat = sum(p[1] for p in coords) / len(coords)
    candidates = []
    for d in COPPERBELT_DEPOSITS:
        if commodity != "multi" and d.commodity != commodity: continue
        dist = _haversine(center_lat, center_lon, d.lat, d.lon)
        base = max(0.1, 1.0 - (dist / 120.0))
        score = min(0.98, base * (1.15 if d.commodity == commodity else 0.9))
        candidates.append({"name": d.name, "lat": d.lat, "lon": d.lon, "commodity": d.commodity, "score": round(score, 3), "confidence": round(0.75 + (score * 0.2), 2)})
    candidates.sort(key=lambda x: -x["score"])
    top = candidates[:n_targets]
    targets = [ProspectivityTarget(id=i, name=t["name"], lat=t["lat"], lon=t["lon"], score=t["score"], commodity=t["commodity"], confidence=t["confidence"], key_features={"dist_to_known_km": 5.0}) for i, t in enumerate(top)]
    return PredictResponse(run_id=42, targets=targets, summary=f"Demo model — strong signals near known {commodity} deposits", map_geojson=None, confidence_overall=0.82)