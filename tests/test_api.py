import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_projects():
    r = client.get("/api/v1/projects")
    assert r.status_code == 200

def test_predict_contract():
    aoi = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[27.6,-12.3],[28.1,-12.3],[28.1,-12.7],[27.6,-12.7],[27.6,-12.3]]]}}]}
    r = client.post("/api/v1/predict", json={"aoi_geojson": aoi, "commodity": "Cu"})
    assert r.status_code == 200
    data = r.json()
    assert "targets" in data