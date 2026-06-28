"""
Weather API router.
Proxies Open-Meteo with caching and professional metadata.

Endpoints support AOI centroid or specific point queries.
"""

from fastapi import APIRouter, Query, Depends
from typing import Optional

from backend.app.services.weather import get_weather
from backend.app.core.security import get_current_user

router = APIRouter()


@router.get("/weather", tags=["weather", "real-time"])
async def get_weather_for_location(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    days: int = Query(7, ge=1, le=16, description="Forecast days"),
    user: str = Depends(get_current_user),
):
    """
    Get current weather + forecast for a point (e.g. AOI centroid or clicked location).

    Includes:
    - Current: temp, humidity, precip, wind, weather code, etc.
    - Hourly and daily forecast.
    - Metadata: source, fetched_at timestamp, units, notes.

    Critical for field safety and planning (drones, access, heat/dust/flood).
    Data from Open-Meteo (free, accurate global models).
    """
    data = await get_weather(lat, lon, days)
    return data


@router.get("/weather/aoi-summary", tags=["weather"])
async def get_aoi_weather_summary(
    # For demo, accept simple lat/lon. In full, could accept project_id and fetch centroid from DB.
    lat: float = Query(..., description="AOI centroid latitude"),
    lon: float = Query(..., description="AOI centroid longitude"),
    user: str = Depends(get_current_user),
):
    """Convenience for project AOI weather context."""
    return await get_weather(lat, lon, days=3)  # short forecast for ops