from sqlmodel import SQLModel, Field

from geoalchemy2 import Geometry

from typing import Optional
from datetime import datetime

class Project(SQLModel, table=True):
    __tablename__ = "projects"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    country: str = "Zambia"
    commodity: str = "Cu"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    aoi_wkt: Optional[str] = None
    aoi_geom: Optional[str] = Field(default=None, sa_column=Geometry('POLYGON', srid=4326))
    analyses_count: int = 0

class MineralOccurrence(SQLModel, table=True):
    __tablename__ = "mineral_occurrences"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    commodity: str
    latitude: float
    longitude: float
    region: str = "Copperbelt"
    deposit_type: Optional[str] = None
    geom: Optional[str] = Field(default=None, sa_column=Geometry('POINT', srid=4326))

class ProspectivityRun(SQLModel, table=True):
    __tablename__ = "prospectivity_runs"
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    aoi_geojson: str
    model_name: str = "demo_xgb_v0"
    status: str = "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    results_json: Optional[str] = None