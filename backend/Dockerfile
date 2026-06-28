FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps for geo libs (geopandas/fiona for shapefile/GeoJSON) + postgis client
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    libgeos-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast installs (or fall back to pip)
RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
# Copy lock if present (uv.lock preferred when committed)
# COPY uv.lock ./

RUN uv pip install --system -e "[dev]" --no-cache || \
    pip install --no-cache-dir -e "[dev]"

COPY . .

# Default command overridden in compose
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]