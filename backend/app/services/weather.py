"""
Weather integration service using Open-Meteo (free, no key, high quality).

Provides current conditions + forecast for a lat/lon.
Includes caching with timestamps for demo/professional use.
Key variables for mining/exploration: temp, precip, wind, etc.

See DEVELOPMENT_LOOP.md for professional context (field safety, access, drone ops).
"""

import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json

# Simple in-memory cache for demo. In prod use Redis.
_cache: Dict[str, Dict[str, Any]] = {}

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Variables we care about for ops
CURRENT_VARS = "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m"
HOURLY_VARS = "temperature_2m,precipitation,wind_speed_10m"
DAILY_VARS = "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"


def _cache_key(lat: float, lon: float, days: int = 7) -> str:
    return f"{lat:.4f},{lon:.4f},{days}"


async def get_weather(lat: float, lon: float, days: int = 7) -> Dict[str, Any]:
    """
    Fetch current + forecast from Open-Meteo.
    Caches responses for ~10 min.
    Returns structured data with timestamps and source metadata.
    """
    key = _cache_key(lat, lon, days)
    now = datetime.utcnow()

    if key in _cache:
        cached = _cache[key]
        if (now - cached["fetched_at"]).total_seconds() < 600:  # 10 min cache
            return cached["data"]

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": CURRENT_VARS,
        "hourly": HOURLY_VARS,
        "daily": DAILY_VARS,
        "timezone": "auto",
        "forecast_days": min(days, 16),
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(OPEN_METEO_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    # Enrich with metadata
    result = {
        "latitude": lat,
        "longitude": lon,
        "source": "Open-Meteo (ECMWF/NOAA models)",
        "fetched_at": now.isoformat() + "Z",
        "units": data.get("current_units", {}),
        "current": data.get("current", {}),
        "hourly": data.get("hourly", {}),
        "daily": data.get("daily", {}),
        "note": "Real-time weather for field/ops planning. Always verify with on-site meteorological stations.",
    }

    _cache[key] = {"data": result, "fetched_at": now}
    return result


def get_weather_sync(lat: float, lon: float, days: int = 7) -> Dict[str, Any]:
    """Sync wrapper for places that can't await (e.g. simple scripts)."""
    import asyncio
    return asyncio.run(get_weather(lat, lon, days))