# GeoVision AI — Iterative Development Loop

**Repository**: `karanja-droid/geovision-ai`  
**Goal**: Build a complete, production-ready web platform that uses AI and geospatial data to identify and rank high-potential mineral exploration targets (starting with Copper, Cobalt, and Lithium) across Southern Africa.  
**Status**: Repository is currently empty — this loop will take us from zero to deployed MVP and beyond in a structured, trackable way on GitHub.

---

## 1. Vision & Success Criteria

**Core Value Proposition**  
GeoVision AI helps geologists, exploration companies, and investors in Southern Africa move faster from regional data to drill-ready targets by combining:
- Multi-layer geospatial data (geology, structure, geophysics, remote sensing, geochemistry)
- Modern machine learning / AI prospectivity modeling
- Beautiful, interactive visualizations and ranked target lists
- Actionable reports and project memory

**MVP Success (v0.5 – v1.0)**  
A logged-in user can:
1. Create/select a project and define an Area of Interest (AOI) in Zambia, DRC, Zimbabwe, Tanzania, or Mozambique
2. Run an AI prospectivity model (initially for Copper or multi-commodity)
3. See an interactive map with:
   - Prospectivity heatmap / probability surface
   - Known mineral occurrences overlaid
   - Top 10–20 ranked exploration targets
4. Adjust parameters and re-run
5. Export results (GeoJSON + PDF report)
6. Save the analysis to their project history

**Longer-term Vision**  
SaaS platform with team workspaces, advanced models (deep learning, ensembles, Earth Engine integration), API access, and continuous model improvement from new exploration results.

---

## 2. The GeoVision Development Loop (Core Framework)

We use **nested loops** inspired by agile + lean startup + domain-driven design, optimized for a solo technical founder with strong data science background.

### Macro Loop (Release Cycle)
Run this every **4–8 weeks**:

```mermaid
flowchart TD
    A[Start New Release Cycle] --> B[Review Backlog + Define 3–6 Key Goals for this Release]
    B --> C[Prioritize & Break into Issues + Assign to Milestone]
    C --> D[Execute Multiple Inner Feature Loops]
    D --> E[Integration Testing + End-to-End Validation on Real Southern Africa Use Cases]
    E --> F[Staging Deployment + Self QA / Demo Recording]
    F --> G[Production Release + Changelog + Announcement]
    G --> H[Collect Feedback (even solo: what felt slow, what gave most insight)]
    H --> I[Update Metrics, Backlog & Technical Debt List]
    I --> A
```

### Inner Feature Loop (for every major capability)
Use this micro-loop for each feature or user story (1–5 days typical):

1. **Understand & Design** (½–1 day)  
   - Write or refine the GitHub issue with acceptance criteria  
   - Quick wireframe (Excalidraw, Figma, or even hand-drawn photo)  
   - Define data model changes + API contract (request/response examples)  
   - Note any new geospatial or ML considerations

2. **Implement Core Logic** (backend + AI first)  
   - Work on feature branch `feature/xxx`  
   - Add or update DB models/migrations  
   - Implement service layer (geospatial processing, model inference)  
   - Write unit + integration tests

3. **Build Visualization / UX Layer**  
   - Streamlit page or component  
   - Interactive map elements  
   - Forms, filters, feedback UI

4. **Test & Domain Validate**  
   - Run on real or realistic Southern Africa data (Copperbelt example first)  
   - Check that outputs make geological sense (e.g., high probability near known deposits and structures)  
   - Performance & edge cases (large AOI, missing data layers)

5. **Polish, Document & Demo**  
   - Code quality (ruff, mypy)  
   - Update README / docs / docstrings  
   - Record a 60–90s Loom or add screenshots to the PR  
   - Link issue in PR description ("Closes #42")

6. **Review & Merge**  
   - Self-review checklist or future collaborator review  
   - Merge to `main` (protected) → triggers CI/CD

7. **Close the Loop**  
   - Move issue to Done on Project board  
   - Add any learnings or follow-up issues (e.g., "improve model explainability")

---

## 3. Recommended Tech Stack (Optimized for Speed + Power)

| Layer              | Choice                          | Why |
|--------------------|----------------------------------|-----|
| **Backend**        | FastAPI + Uvicorn               | Async, auto OpenAPI docs, Pydantic, perfect for AI services |
| **Database**       | PostgreSQL 16 + PostGIS 3.4     | Industry standard for geospatial; powerful spatial queries & indexing |
| **ORM / Models**   | SQLModel (Pydantic v2 + SQLAlchemy) + Alembic | Type-safe, great DX with FastAPI |
| **Geospatial**     | GeoPandas, Shapely, Rasterio, rioxarray, pyproj | Mature, fast, handles both vector & raster |
| **ML / AI**        | scikit-learn, XGBoost, LightGBM (start)<br>PyTorch (later for DL) | Interpretable baseline models first; easy to productionize with ONNX/Joblib |
| **Frontend**       | **Streamlit** (MVP & v1)        | Extremely fast iteration for data/AI apps. Excellent map support via `st_folium`, `pydeck`, `keplergl`. Can call your FastAPI. |
| **Styling / UI**   | Streamlit native + custom CSS or `streamlit-extras` | Good enough for professional internal/SaaS feel initially |
| **Auth**           | FastAPI Users (or simple JWT) + Streamlit integration | Quick to add user/project isolation |
| **Deployment**     | Docker + Docker Compose locally<br>Render.com / Fly.io / Railway (staging & prod) | Excellent free tiers + GitHub integration |
| **CI/CD**          | GitHub Actions                  | Lint, test, build Docker image, deploy |
| **Tooling**        | `uv` (Python packaging), `ruff` (lint+format), `mypy`, `pytest`, `pre-commit` | Blazing fast modern Python DX |
| **Versioning**     | Git + semantic tags + GitHub Releases | Clear history |

**Future Upgrades (when needed)**:
- Replace/ complement Streamlit frontend with React + MapLibre GL JS + shadcn/ui for pixel-perfect SaaS look
- Add Celery / RQ or FastAPI BackgroundTasks for long-running inference
- Integrate Google Earth Engine or Microsoft Planetary Computer for live satellite indices
- Add MLflow or Weights & Biases for experiment tracking

---

## 4. Phased Roadmap (Looped Sprints)

### Phase 0: Foundation (Week 1) — Milestone: `mvp-foundation`
**Goal**: Working local environment + basic project hygiene

**Key Issues / Tasks**:
- Project structure & `pyproject.toml` / `uv.lock`
- `docker-compose.yml` (postgres-postgis, backend, streamlit, optional pgadmin)
- FastAPI skeleton (`/health`, `/docs`, CORS, settings via pydantic)
- Streamlit skeleton app with sidebar navigation
- GitHub setup: labels, Project board (Kanban), Milestones, Issue templates
- `.github/workflows/ci.yml` (ruff, mypy, pytest)
- Initial README + this `DEVELOPMENT_LOOP.md`
- Basic `.gitignore`, LICENSE (MIT or your choice), CODEOWNERS

### Phase 1: Data Layer & Projects (1–2 weeks) — Milestone: `data-foundation`
**Goal**: Users can create projects and manage AOIs + known deposits

- Domain models: `User`, `Project`, `AreaOfInterest` (with geometry), `MineralOccurrence` (known deposits)
- PostGIS spatial indexes + GeoAlchemy2 or geometry columns
- Ingestion endpoints/services: upload GeoJSON/Shapefile, draw AOI on map (or paste WKT/GeoJSON)
- Demo data loader (synthetic or simplified public Copperbelt geology + known deposits)
- CRUD APIs + Streamlit pages for project management
- Basic spatial queries (e.g., deposits inside AOI)

### Phase 2: AI Prospectivity Engine (2–3 weeks) — Milestone: `ai-core`
**Goal**: Run meaningful prospectivity models and return ranked targets

- Feature store / engineering service (spatial joins, buffer distances to faults, zonal statistics on rasters, lithology encoding, etc.)
- Training pipeline (notebook + script) using known deposits as positive labels + random or stratified negative sampling
- Baseline model (XGBoost / RandomForest) persisted with joblib or ONNX
- Inference endpoint: `POST /api/v1/predict` → returns probability raster or vector targets + metadata
- Simple explainability (feature importances, partial dependence)
- Versioning of models + association with Project runs
- Validation against held-out known deposits (precision@K, AUC, etc.)

**Southern Africa Focus First**: Copperbelt (Zambia/DRC) — high data density and clear structural controls.

### Phase 3: Interactive Maps & Dashboard (2 weeks) — Milestone: `visualization`
**Goal**: Beautiful, insightful map experience that drives decisions

- Main Streamlit page with:
  - Project/AOI selector
  - Interactive map (folium or pydeck) showing:
    - Base layers (OpenStreetMap, satellite)
    - Known deposits (color by commodity: Cu=blue, Co=green, Li=purple)
    - Prospectivity surface (heatmap or classified raster)
    - Top targets as markers with popups (score, key features, distance to infrastructure if available)
  - Controls: probability threshold slider, commodity filter, re-run model button
  - Side panel: ranked target table (sortable, exportable)
- Additional charts (Plotly): score distribution, feature importance
- Caching of expensive computations (`@st.cache_data`, `@st.cache_resource`)

### Phase 4: Polish, Reporting & Auth (1–2 weeks) — Milestone: `mvp-polish`
- User authentication & project ownership (multi-user ready)
- PDF report generation (map image + summary + methodology + top targets table)
- Export GeoJSON / Shapefile of results
- Demo mode / sample Copperbelt project for new users
- Error handling, loading states, helpful empty states
- Mobile responsiveness improvements
- Onboarding flow / help tooltips

### Phase 5: DevOps, Testing & Deployment (1 week) — Milestone: `production-ready`
- Comprehensive test suite (unit for services, integration with test PostGIS)
- GitHub Actions full pipeline (CI on every PR + CD on merge to main → staging, manual prod deploy)
- Docker production images (multi-stage, non-root)
- Environment configs (dev/staging/prod)
- Basic monitoring hooks (logging, health checks)
- Security hardening (file upload validation, rate limiting, secrets management)
- Deploy first version to Render/Fly.io/Railway

### Phase 6+: Continuous Improvement Loop (Ongoing)
After MVP launch, the loop continues with higher-value iterations:
- Earth Engine / Sentinel-2 integration for alteration mapping (iron oxide, clay, etc.)
- More advanced models (ensembles, Bayesian ML, GNNs, or CNNs on imagery)
- Collaboration features (share project, comment on targets)
- API for external tools / partners
- Performance at scale (tile server for large rasters, caching, async inference)
- Business features if SaaS path (quotas, billing, team workspaces)
- New regions & commodities based on your business deals (e.g., Tanzania sulphur corridor synergies, Mozambique, etc.)

---

## 5. GitHub Workflow & Project Management (How the Loop Lives in GitHub)

1. **GitHub Projects** (recommended: Board view)  
   Columns: `Backlog` → `Ready` → `In Progress` → `Review` → `Done`

2. **Labels** (create these):
   - `type:feature`, `type:bug`, `type:docs`, `type:devops`
   - `component:backend`, `component:frontend`, `component:ai-ml`, `component:geospatial`, `component:data`
   - `priority:P0`, `priority:P1`, `priority:P2`
   - `size:XS`, `size:S`, `size:M`, `size:L`
   - `region:southern-africa`, `mineral:cu`, `mineral:co`, `mineral:li`
   - `status:blocked`, `status:needs-design`

3. **Milestones**  
   Map directly to the Phases above (`mvp-foundation`, `ai-core`, etc.)

4. **Branching Strategy** (lightweight Git Flow)
   - `main` is always deployable
   - `feature/xxx-short-description`
   - `fix/yyy`
   - Delete branches after merge

5. **Pull Request Template** (we can create `.github/PULL_REQUEST_TEMPLATE.md`)
   - Link to issue(s)
   - Screenshots / Loom for UI changes
   - Test evidence (especially model validation on real geology)
   - Checklist (tests pass, ruff clean, docs updated)

6. **GitHub Actions** (we will generate)
   - `ci.yml`: lint, type-check, test (with PostGIS service container)
   - `deploy-staging.yml` / `deploy-prod.yml`

---

## 6. Immediate Next Steps (Start Today)

1. **Initialize the repository locally** (if not done):
   ```bash
   git clone https://github.com/karanja-droid/geovision-ai.git
   cd geovision-ai
   git checkout -b setup/foundation
   ```

2. **Copy this file** into `docs/DEVELOPMENT_LOOP.md` in your repo.

3. **Create the GitHub Project board**, labels, and first milestone (`mvp-foundation`).

4. **Tell me what to generate next** (I can create all starter files instantly):
   - Full recommended folder structure + key files (`docker-compose.yml`, `backend/app/main.py`, Streamlit `app.py`, DB models, sample prospectivity training code, GitHub Actions, etc.)
   - Specific Phase 0 scaffolding package
   - AI model example notebook focused on Copperbelt
   - Architecture diagram (mermaid or PlantUML)
   - Anything else

This loop is designed so that every cycle produces **visible progress** you can demo, while keeping technical debt low and the codebase clean for future collaborators or investors.

Ready when you are, Peter. Let's build GeoVision AI systematically and ship something impressive.

---

*Document generated for karanja-droid/geovision-ai — June 2026*  
*Next update: after Phase 0 completion*