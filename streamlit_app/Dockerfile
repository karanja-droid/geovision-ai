FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
RUN uv pip install --system -e ".[dev]" --no-cache || \
    pip install --no-cache-dir -e ".[dev]"

COPY . .

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]