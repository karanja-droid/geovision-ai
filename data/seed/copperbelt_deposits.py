from dataclasses import dataclass
from typing import List

@dataclass
class DemoDeposit:
    name: str
    lat: float
    lon: float
    commodity: str
    region: str = "Copperbelt"

COPPERBELT_DEPOSITS: List[DemoDeposit] = [
    DemoDeposit("Konkola", -12.39, 27.80, "Cu"),
    DemoDeposit("Nchanga", -12.52, 27.85, "Cu"),
    DemoDeposit("Mufulira", -12.55, 28.25, "Cu"),
    DemoDeposit("Lumwana", -12.25, 25.85, "Cu"),
    DemoDeposit("Bikita Li", -19.95, 31.45, "Li"),
]

def get_deposits_geojson():
    return {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"id": i, "name": d.name, "commodity": d.commodity}, "geometry": {"type": "Point", "coordinates": [d.lon, d.lat]}} for i, d in enumerate(COPPERBELT_DEPOSITS)]}