# GeoVision AI — Iterative Development Loop (Updated with Professional Geoscience & Real-Time Data)

**Repository**: `karanja-droid/geovision-ai`  
**Goal**: Build a complete, production-ready web platform that uses AI and geospatial data to identify and rank high-potential mineral exploration targets (starting with Copper, Cobalt, and Lithium) across Southern Africa. Designed for **geologists, geoscientists, and metallurgists** with high-accuracy, real-time capable data layers for operational decision-making.  
**Status**: Repository initialized with core documentation. This updated version incorporates critical real-time weather, detailed mining geology layers, infrastructure, and professional data standards for field and office use.  
**Last Updated**: June 2026

---

## 1. Vision & Success Criteria (Enhanced for Professional Users)

**Core Value Proposition**  
GeoVision AI accelerates mineral exploration and supports operational decisions in Southern Africa by integrating:
- High-quality, provenance-tracked geospatial data (geology, geophysics, geochemistry, remote sensing, known deposits)
- AI-driven prospectivity modeling with explainability
- **Real-time and contextual weather** for field safety, planning (drone flights, access, dust/heat/flood risks), and operations
- Interactive maps with rich querying, metadata, and layered analysis tailored for geologists and metallurgists
- Actionable outputs: ranked targets, reports, and exportable data with full attribution

**MVP Success (v0.5 – v1.0) – Professional Grade**  
A logged-in user (geologist/metallurgist) can:
1. Create/select a project and define an Area of Interest (AOI) in Zambia, DRC, Zimbabwe, Tanzania, Mozambique, or broader Southern Africa
2. View and toggle multiple critical data layers on an interactive map with **full metadata, sources, update timestamps, resolution/accuracy notes, and legends**
3. Query any feature (click map) for rich popups: rock type descriptions, assay values, deposit details (commodity, grade/tonnage if available, status), model contributions, current weather context
4. Run AI prospectivity models (initially Cu-Co focused on Copperbelt-style systems) incorporating or contextualized by geological layers
5. View **real-time/current weather + short-term forecast** for the AOI or clicked location (temperature, precipitation, wind, conditions) with data source and last update — critical for field deployment planning
6. Overlay infrastructure (roads, power, water) and terrain analysis for logistics and access assessment
7. Adjust parameters, re-run models, and export results (GeoJSON, PDF report with methodology, data sources, weather snapshot, and ranked targets)
8. Save analyses with versioned input data snapshots for auditability

**Professional Credibility Features**:
- Every layer displays provenance (source, vintage/date, resolution/scale, methodology for derived products, license/attribution, known limitations/uncertainty)
- Support for uploading user-specific data (e.g., proprietary assays, new drill results, custom geology interpretations)
- Real-time elements clearly timestamped with refresh capability
- Designed for integration into workflows of national geological surveys, junior explorers, and operating mines

**Longer-term Vision**  
SaaS platform with team collaboration, advanced multi-modal AI (including temporal/weather context where relevant), API access for external tools, continuous model improvement from user-validated results, and deeper integration with national data portals (e.g., Zambian GSD digital database).

---

## 2. The GeoVision Development Loop (Core Framework)

(Framework remains the same as original — nested Macro Release + Inner Feature loops. Updates below focus on data and visualization priorities for professional geoscience use.)

### Macro Loop (Release Cycle)
Run this every **4–8 weeks** (same structure).

### Inner Feature Loop (for every major capability)
Emphasize in **Understand & Design** and **Test & Domain Validate** steps:
- Consult domain experts or literature for Copperbelt (Lufilian Arc structures, Katangan Supergroup lithologies, redox controls on Cu-Co) and other systems (e.g., lithium pegmatites).
- Validate outputs against known deposits and geological reasonableness.
- Include weather context in field-oriented testing scenarios.

---

## 3. Recommended Tech Stack (Optimized for Speed + Power + Professional Data Handling)

| Layer              | Choice                          | Why (including professional geoscience needs) |
|--------------------|----------------------------------|-----|
| **Backend**        | FastAPI + Uvicorn               | Async, auto OpenAPI docs, Pydantic; easy proxy/caching for weather APIs and WMS |
| **Database**       | PostgreSQL 16 + PostGIS 3.4     | Spatial queries, indexing for large vector datasets (deposits, faults, licenses); store layer metadata |
| **ORM / Models**   | SQLModel + Alembic             | Type-safe models with spatial extensions |
| **Geospatial**     | GeoPandas, Shapely, Rasterio, rioxarray, pyproj, rasterstats | Full vector/raster processing; zonal stats for feature engineering; support for uploads and on-the-fly processing |
| **Remote Sensing** | Integration with Sentinel Hub / Planetary Computer or local COG processing | Dynamic or cached Sentinel-2 / Landsat scenes and derived indices (iron oxide, clay, vegetation) for alteration mapping |
| **ML / AI**        | scikit-learn, XGBoost, LightGBM (baseline); PyTorch (later) | Interpretable models; feature importance tied to geological variables; optional inclusion of terrain/weather-derived features |
| **Weather Integration** | Open-Meteo (primary, free, no key) + fallback to OpenWeatherMap | Real-time current conditions, hourly/daily forecasts, historical reanalysis (ERA5). High accuracy, global coverage. Cache responses with timestamps. Variables: temp, precip, wind speed/direction, humidity, etc. |
| **Frontend**       | **Streamlit** (MVP & v1) or migrate to React + MapLibre GL JS | Streamlit excellent for rapid data viz and map layers (`st_folium`, `pydeck`, custom components). MapLibre for advanced professional cartography if scaling to full SPA. Layer control, legends, popups, time-aware if needed. |
| **Mapping**        | Folium / ipyleaflet / pydeck / MapLibre | Support for WMS/WMTS overlays (geological maps if available), vector layers, raster heatmaps/tiles, click queries, drawing AOIs |
| **Styling / UI**   | Streamlit + custom or shadcn/ui (later) | Professional legends, collapsible layer groups, metadata panels, weather widget |
| **Auth & Projects**| FastAPI Users / JWT + project versioning | Multi-user, save versioned analyses with data snapshots |
| **Deployment**     | Docker + Docker Compose; Render/Fly.io/Railway | Easy scaling; background tasks for processing |
| **CI/CD & Tooling**| GitHub Actions, `uv`, `ruff`, `mypy`, `pytest`, `pre-commit` | Quality and automation |
| **Additional**     | Redis (caching weather & processed tiles), Celery/RQ (async tasks) | Performance for real-time elements and heavy raster processing |

**Data Standards Emphasis**:
- All ingested or derived layers include metadata tables/attributes: source, update_date, resolution, accuracy_notes, citation.
- Support OGC standards where possible (WMS for base geology if available from national surveys).

---

## 4. Phased Roadmap (Looped Sprints) — Updated with Critical Data Layers

### Phase 0: Foundation (Week 1) — Milestone: `mvp-foundation`
(As before, plus:)
- Set up weather proxy endpoint in FastAPI (Open-Meteo integration with caching and timestamping).
- Basic map with layer control skeleton and metadata display component.
- Initial data ingestion scripts for key public datasets (see Phase 1).

### Phase 1: Data Layer & Projects (1–2 weeks) — Milestone: `data-foundation`
**Goal**: Robust, provenance-tracked data foundation with critical mining geology, infrastructure, and weather capabilities.

**Priority Critical Datasets & Layers** (ingest or proxy; prioritize free/public first):

**1. Known Mineral Deposits & Occurrences (Core for validation & context)**
   - Sources: USGS "Compilation of Geospatial Data (GIS) for the Mineral Industries... of Africa" (mineral occurrence sites, exploration/development sites, production facilities); RCMRD Africa Major Mineral Deposits; Zambian GSD mineral occurrence database/maps; Mindat.org or national equivalents where accessible.
   - Attributes: Location (point/polygon), commodity (Cu, Co, Li prioritized), deposit type/style, grade/tonnage/resources if available, status (occurrence/prospect/mine), host rock/lithology, structural controls, source, last_update, confidence/accuracy notes.
   - Implementation: PostGIS table with spatial index; styled by commodity/color in map.

**2. Geology & Lithology**
   - Bedrock/surface lithology: Africa Surface Lithology (ISRIC/compilations), Zambian 1:1M or 1:2M geological maps (GSD), regional compilations.
   - Structures: Faults, shears, lineaments, folds (critical for Copperbelt Lufilian Arc tectonics and fluid pathways) — from national surveys or derived from geophysics/RS.
   - Attributes: Rock type/name, age/formation, description, alteration potential, source metadata.

**3. Geophysics (key for prospectivity)**
   - Magnetic (total magnetic intensity, derivatives like RTP, analytic signal) — high value for delineating structures and intrusions.
   - Gravity (Bouguer, residual).
   - Radiometric (K, Th, U channels) where available.
   - Sources: National geological surveys (Zambia GSD digital database), commercial compilations (e.g., Getech if licensed later), or user-uploaded grids.
   - Storage/handling: Raster (GeoTIFF/COG) or vector; support upload and basic processing (e.g., hillshade-like derivatives).

**4. Geochemistry**
   - Soil, stream sediment, rock chip, drill core assays.
   - Multi-element; pathfinder indices; interpolated grids or point data.
   - Support upload of assay tables with coordinates + automated spatial join or interpolation.

**5. Remote Sensing & Alteration Mapping (dynamic/high value)**
   - Sentinel-2 (or Landsat) scenes/indices: True/false color, iron oxide (ferric), clay/sericite (SWIR), NDVI/vegetation, etc.
   - Integration: Backend calls to Sentinel Hub / Microsoft Planetary Computer or cached local processing. Allow on-demand computation for AOI.
   - Critical for identifying hydrothermal alteration halos around deposits.

**6. Topography, Terrain & Hydrology**
   - DEM (SRTM 30m or higher-res ALOS/ASTER where available).
   - Derived: Slope, aspect, hillshade, curvature, drainage networks, watersheds.
   - Use: Access planning, erosion/landslide risk, site suitability.

**7. Infrastructure & Logistics (operational critical)**
   - From USGS Africa compilation: Major roads, railways, power lines/transmission, power plants, ports, airports, major cities/towns, rivers/lakes.
   - Additional: Water sources, existing mines/processing plants/tailings (where public).
   - Enables cost modeling, access assessment, and risk evaluation (e.g., distance to power/road for new targets).

**8. Tenure, Regulatory & Environmental (real-use essential)**
   - Mining licenses/concessions (polygons) — initially via user upload or sample data; later integration with national cadastres if APIs available.
   - Protected areas, environmental sensitivities, land use.
   - Critical for legal/permitting context.

**9. Weather & Environmental Context (real-time / near real-time)**
   - **Integration**: FastAPI endpoint proxying Open-Meteo (recommended primary: free, accurate, no key, global models including high-res regional).
     - Current conditions for point or AOI centroid.
     - Hourly + daily forecast (7–16 days).
     - Historical context (e.g., recent precipitation totals, temperature extremes, or ERA5 climatology).
   - Key variables for mining/exploration ops: Temperature (heat stress), Precipitation (access, flooding, dust suppression), Wind speed/direction (drone/UAV safety, dust), Humidity, UV index, visibility.
   - Display: Sidebar widget or map overlay (e.g., weather icons or simple raster if relevant); timestamp ("Data from Open-Meteo ECMWF model, last updated: [time]"); refresh button.
   - Caching: Short-term cache (minutes) with clear "as of" indicators for accuracy.
   - Fallback/Alternative: OpenWeatherMap for additional features (alerts, maps).
   - Professional note: Weather is dynamic — always show source, model, update time, and any known limitations. Not a substitute for on-site meteorological stations.

**Data Ingestion & Management**:
- Scripts/notebooks for bulk import of public datasets (USGS geodatabase, RCMRD, etc.).
- User upload support for custom layers (GeoJSON, Shapefile via geopandas, GeoTIFF via rasterio) with automatic metadata capture.
- Layer metadata registry in DB (source, date, resolution, accuracy, citation, geometry_type).
- Versioning and snapshots for analyses.

**Southern Africa / Copperbelt Focus First**:
- Prioritize Lufilian Arc structures, Katangan Supergroup lithologies (Ore Shale, etc.), known sediment-hosted Cu-Co deposits, redox boundaries, and associated Co enrichment.
- Expand to lithium (pegmatites in Zimbabwe, etc.) and other critical minerals in subsequent iterations.

### Phase 2: AI Prospectivity Engine (2–3 weeks) — Milestone: `ai-core`
(As before, plus enhancements:)
- Feature engineering explicitly draws from the critical layers above (lithology one-hot or embeddings, distance to faults/structures, proximity to known deposits as spatial features, terrain derivatives, geophysical anomaly values via zonal stats, RS indices).
- Optional: Contextual weather-derived features if they add signal (e.g., rainfall patterns influencing supergene enrichment or access — secondary priority).
- Model outputs: Probability/favorability raster + vector targets with confidence scores, key contributing features (explainability via SHAP or permutation importance — geologist-friendly), uncertainty estimates.
- Validation: Against held-out known deposits; geological reasonableness checks.
- Storage: Associate runs with specific data versions/snapshots.

### Phase 3: Interactive Maps & Dashboard (2 weeks) — Milestone: `visualization`
**Goal**: Professional-grade interactive map experience with rich querying, layered analysis, and operational weather context.

**Map Implementation**:
- Base: Satellite imagery + OSM/topo.
- **Layer Groups** (collapsible, toggleable, opacity control, legends):
  - **Geology**: Lithology polygons, structures (faults/lines with styling by type/age).
  - **Deposits & Mineralization**: Points/polygons styled by commodity/status; size by importance/grade.
  - **Geophysics & Geochem**: Raster overlays or classified vectors; point data with value popups.
  - **Remote Sensing**: Toggleable indices or scene composites.
  - **Terrain & Infrastructure**: DEM hillshade + vector overlays (roads, power, water) with distance calculations possible.
  - **Tenure & Constraints**: License polygons, protected areas.
  - **AI Prospectivity**: Heatmap or classified raster + target points (clickable with scores and top features).
  - **Weather**: Current conditions panel/widget (for AOI or map center/click); optional simple overlays (e.g., precip if rasterized). Forecast summary. Clear "real-time / last updated" indicators.

**Interactive Features for Geoscientists**:
- **Click Query / Identify Tool**: Rich popups showing all intersecting layer attributes + synthesized view (e.g., "At this location: Lithology = [type] (source: GSD 1:250k, updated 2023); Nearest known deposit: [name] (Cu-Co, 2.5% Cu); Current weather: 28°C, light rain, wind 12 km/h from SE (Open-Meteo, updated 5 min ago); Prospectivity score: 0.78 (key drivers: proximity to fault X, favorable lithology)").
- Drawing tools for custom AOIs or target polygons.
- Filters and queries (e.g., deposits with >X% grade, areas with high prospectivity + slope <15° + within 5km of road).
- Time-aware elements where applicable (e.g., recent Sentinel scenes).
- Charts/Stats panel: Summary stats for AOI (area, % covered by favorable lithology, number of known occurrences, average weather metrics, etc.).
- Export: Selected layers or full view as GeoPackage/GeoJSON + PDF report embedding map image, weather snapshot, methodology, data sources/attributions, and ranked targets table.

**Performance & Accuracy**:
- Tile caching or COG support for rasters.
- Vector simplification for performance on large datasets.
- Clear visual distinction between static (geology) and dynamic (weather) layers.
- Loading indicators and error handling with data quality notes.

### Phase 4: Polish, Reporting & Auth (1–2 weeks) — Milestone: `mvp-polish`
(As before +)
- Reports include comprehensive data sources section, weather context at time of analysis, layer metadata summary, and disclaimers on accuracy/real-time nature.
- Onboarding with sample Copperbelt project pre-loaded with key layers.

### Phase 5: DevOps, Testing & Deployment (1 week) — Milestone: `production-ready`
(As before + emphasis on)
- Testing includes data layer accuracy checks, weather API integration tests, query functionality, and professional user scenarios (e.g., "geologist planning field visit checks weather + access layers").
- Monitoring for data freshness where relevant.

### Phase 6+: Continuous Improvement Loop (Ongoing)
- Deeper integration with national portals (e.g., direct WMS from Zambian GSD or RCMRD if available; automated updates where possible).
- Advanced RS processing and multi-temporal analysis.
- User-contributed data validation workflows.
- Potential inclusion of more real-time elements (e.g., seismic if relevant, or satellite tasking alerts).
- Model improvements informed by metallurgical/domaining feedback (e.g., linking prospectivity to processing characteristics).

---

## 5. GitHub Workflow & Project Management

(Same as original, with added labels if useful: e.g., `data:weather`, `data:geology`, `data:deposits`, `professional:geoscience`.)

---

## 6. Immediate Next Steps (Start Today)

1. Review the pushed `docs/DEVELOPMENT_LOOP.md` (original) and this updated version.
2. Create GitHub Project board, labels, and milestone `mvp-foundation`.
3. **Next generation request**: Generate full starter scaffolding including:
   - `docker-compose.yml` with PostGIS
   - FastAPI skeleton with weather endpoint example (Open-Meteo)
   - Basic Streamlit map app with layer control and sample data placeholders
   - Initial data loader scripts for USGS Africa mineral data or simplified Copperbelt deposits
   - DB models for layers/metadata
4. Or specify focus (e.g., "generate weather integration code", "sample data ingestion for deposits", "detailed layer metadata schema").

This updated framework ensures GeoVision AI delivers **accurate, contextual, real-time-capable data** that geologists, geoscientists, and metallurgists can trust for serious exploration and operational decisions in Southern Africa.

Ready to implement the next pieces, Peter. Let's make the map and data layers world-class for professional use.

---

*Document generated/updated for karanja-droid/geovision-ai — June 2026*  
*Incorporates public data sources (USGS Africa mineral geodatabase, RCMRD, Open-Meteo, national surveys) and professional geoscience best practices.*