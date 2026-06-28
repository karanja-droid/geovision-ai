"""
GeoVision AI — Streamlit MVP (Phase 0 + early Phase 3 per DEVELOPMENT_LOOP.md)

Full user flow implemented for demo.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os

st.set_page_config(page_title="GeoVision AI", layout="wide", page_icon="🌍")

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

@st.cache_data(ttl=60)
def fetch_projects():
    try:
        r = requests.get(f"{BACKEND}/api/v1/projects", timeout=5)
        return r.json()
    except Exception:
        return [{"id": 0, "name": "Copperbelt Demo Project (offline)", "country": "Zambia", "commodity": "Cu"}]

def get_demo_aoi():
    return {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[27.6, -12.3], [28.1, -12.3], [28.1, -12.7], [27.6, -12.7], [27.6, -12.3]]]}}]}

def call_predict(aoi_geojson, commodity="Cu"):
    try:
        r = requests.post(f"{BACKEND}/api/v1/predict", json={"aoi_geojson": aoi_geojson, "commodity": commodity}, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception:
        st.warning("Backend not reachable — using offline demo results.")
        return {"run_id": 424242, "targets": [{"id": 0, "name": "Konkola Deep", "lat": -12.40, "lon": 27.81, "score": 0.91, "commodity": "Cu", "confidence": 0.88, "key_features": {}}], "summary": "Offline demo (calibrated).", "confidence_overall": 0.86}

def deposits_geojson():
    try:
        return requests.get(f"{BACKEND}/api/v1/deposits", timeout=5).json()
    except:
        return {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Konkola", "commodity": "Cu"}, "geometry": {"type": "Point", "coordinates": [27.80, -12.39]}}]}

def generate_pdf_report(project_name, targets, summary):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "GeoVision AI — Prospectivity Report")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 70, f"Project: {project_name}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Summary")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 115, summary[:90])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 145, "Top Targets")
    y = height - 165
    c.setFont("Helvetica", 9)
    for t in targets[:8]:
        c.drawString(50, y, f"{t['name']}: score={t['score']:.2f}")
        y -= 14
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 40, "Demo report — see DEVELOPMENT_LOOP.md")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

st.title("🌍 GeoVision AI — Mineral Prospectivity Explorer")
st.caption("Phase 0 MVP • DEVELOPMENT_LOOP.md")

with st.sidebar:
    st.header("Project & AOI")
    projects = fetch_projects()
    selected = st.selectbox("Project", [p["name"] for p in projects])
    use_demo = st.checkbox("Use Copperbelt Demo AOI", value=True)
    aoi_text = st.text_area("AOI WKT", value="", disabled=use_demo, height=70)
    commodity = st.selectbox("Commodity", ["Cu", "Co", "Li", "multi"])
    if st.button("🚀 Run Prospectivity", type="primary"):
        aoi = get_demo_aoi() if use_demo else {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[27.6,-12.3],[28.1,-12.3],[28.1,-12.7],[27.6,-12.7],[27.6,-12.3]]]}}]}
        with st.spinner("Running..."):
            st.session_state["last_result"] = call_predict(aoi, commodity)
            st.session_state["last_project"] = selected

col1, col2 = st.columns([2,1])
with col1:
    st.subheader("Interactive Map")
    m = folium.Map(location=[-12.5, 27.9], zoom_start=8)
    for feat in deposits_geojson().get("features", []):
        c = feat["geometry"]["coordinates"]
        folium.CircleMarker([c[1], c[0]], radius=5, color="blue", popup=feat["properties"].get("name")).add_to(m)
    if "last_result" in st.session_state:
        for t in st.session_state["last_result"].get("targets", []):
            folium.CircleMarker([t["lat"], t["lon"]], radius=7, color="red", popup=t["name"]).add_to(m)
    st_folium(m, height=500)
with col2:
    st.subheader("Results")
    if "last_result" in st.session_state:
        res = st.session_state["last_result"]
        st.success(res.get("summary"))
        for t in res.get("targets", [])[:5]:
            st.write(f"**{t['name']}** score={t['score']:.2f}")
        if st.button("Export GeoJSON"):
            st.download_button("targets.geojson", json.dumps({"type":"FeatureCollection","features":[{"type":"Feature","properties":t,"geometry":{"type":"Point","coordinates":[t["lon"],t["lat"]]}} for t in res["targets"]]}))
        if st.button("Export PDF"):
            pdf = generate_pdf_report(st.session_state.get("last_project","Demo"), res.get("targets",[]), res.get("summary",""))
            st.download_button("report.pdf", pdf, "geovision_report.pdf")
    else:
        st.info("Run analysis from sidebar")

st.caption("Implements DEVELOPMENT_LOOP.md Phase 0. Backend + AI first, then Streamlit viz. Next: Phase 1.")
