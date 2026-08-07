# SENTRIX

SENTRIX is an edge-first multimodal home security system that fuses video, audio, face recognition, behaviour analysis, and cloud threat detection into a 5-level **Threat Confidence Index (TCI)**. It runs entirely on a local machine, falls back gracefully when optional subsystems are unavailable, and escalates incidents automatically through snapshots, encrypted evidence, SMS/call alerts, and emergency dispatch packages.

---

## Feature Overview

| Feature | Status | Notes |
|---|---|---|
| YOLO person detection | ✅ | YOLOv8-nano via `ultralytics` |
| Motion scoring | ✅ | Frame-differencing, no extra model |
| Behaviour classification | ✅ | Heuristic centroid tracking |
| Face authorization | ✅ | `face_recognition` (optional) |
| Person Re-ID | ✅ | DeepSORT + colour histogram fallback |
| Audio anomaly detection | ✅ | `sounddevice` (optional) |
| Cloud weapon/fire detection | ✅ | Roboflow API (optional) |
| Voice SOS ("emergency") | ✅ | VOSK model (optional) |
| TCI fusion + smoothing | ✅ | XGBoost + EMA |
| Explainability panel | ✅ | Top factors, uncertainty, confidence band |
| Threat escalation | ✅ | 5-level policy: snapshot → SMS → siren → evidence → dispatch → call |
| AES-256-GCM evidence | ✅ | HKDF-derived stable key, tamper-detect hash |
| Emergency dispatch | ✅ | Pre-populated form, Twilio SMS |
| HMAC-signed sessions | ✅ | 12-hour token, httponly cookie |
| Upload sanitization | ✅ | Extension + MIME validation, path-traversal safe |
| Auth on all endpoints | ✅ | `/api/*`, `/video`, `/ws/threat`, uploads |
| Async side-effect queue | ✅ | Disk/network I/O off the 30fps hot path |
| Graceful shutdown | ✅ | Thread join, camera release, clean exit |
| DB indexes + retention | ✅ | Fast queries; auto-prune events/snapshots |
| ReID gallery cap | ✅ | FIFO eviction at 200 embeddings |
| Live dashboard | ✅ | WebSocket-driven, TCI gauge, score bars |
| MJPEG video stream | ✅ | `/video` (auth-guarded) |

---

## Architecture

```
                        ┌───────────────────────────────────────┐
                        │          FastAPI App (app.py)          │
                        │  Lifespan: DB init, engines init,      │
                        │  retention prune, bg thread start       │
                        └──────────────┬────────────────────────┘
                                       │
                       ┌───────────────▼────────────────┐
                       │    Background Processing Thread  │  ~30 fps
                       │       SystemEngine.process()    │
                       └──┬──────────────────────────┬──┘
                          │  Hot Path (synchronous)   │
              ┌───────────▼───────────────────────────▼────────────┐
              │ Camera → YOLO → Motion → Behaviour → Audio → Face  │
              │    Cloud Threat → ReID → Fusion → State Update      │
              └───────────────────────┬────────────────────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │   Async Task Queue      │  ← non-blocking
                         │  Worker Thread          │
                         │  snapshot / evidence    │
                         │  SMS / dispatch / DB    │
                         └─────────────────────────┘
```

---

## Directory Structure

```
Sentrix-main/
├── app.py                    # FastAPI entry point, lifespan, processing loop
├── requirements.txt          # Python dependencies
├── .env.example              # Config template
│
├── core/
│   ├── security.py           # HMAC sessions, upload sanitizer
│   ├── system_engine.py      # Per-frame orchestrator + async task queue
│   ├── engine_instance.py    # Engine singleton factory
│   ├── state.py              # Thread-safe shared state (dashboard source of truth)
│   ├── health_monitor.py     # Subsystem availability tracker
│   ├── escalation.py         # 5-level declarative action policy
│   ├── alert_service.py      # Twilio SMS + voice call
│   ├── dispatch_service.py   # Emergency dispatch package builder
│   └── encrypted_evidence.py # AES-256-GCM encryption + HKDF key derivation
│
├── ai/
│   ├── vision_engine.py      # YOLOv8 detection + motion scoring
│   ├── behaviour_engine.py   # Centroid trajectory behaviour classifier
│   ├── audio_engine.py       # Background audio anomaly detector
│   ├── face_engine.py        # Face recognition + authorization persistence
│   ├── reid_engine.py        # Person Re-ID with gallery cap
│   ├── tracking_engine.py    # DeepSORT multi-object tracker
│   ├── cloud_engines.py      # Roboflow cloud weapon/fire inference
│   ├── local_fallback_engine.py # OpenCV weapon heuristic (cloud fallback)
│   ├── fusion_engine.py      # XGBoost TCI fusion + uncertainty + explainability
│   └── voice_sos_engine.py   # VOSK voice command listener
│
├── hardware/
│   ├── camera.py             # Single-camera OpenCV wrapper
│   ├── camera_manager.py     # Multi-camera pool
│   └── siren.py              # Platform-aware alert sound
│
├── db/
│   ├── models.py             # SQLAlchemy ORM (EventLog, DispatchPackage) with indexes
│   └── database.py           # SQLite helper layer + retention prune helpers
│
├── web/
│   ├── routes.py             # Page + API + WebSocket routes (all auth-guarded)
│   └── streaming.py          # MJPEG /video endpoint (auth-guarded)
│
├── templates/                # Jinja2 HTML pages
│   ├── base.html             # Nav + shared assets
│   ├── login.html            # Auth page
│   ├── dashboard.html        # TCI gauge, score bars, explainability, event log
│   ├── live.html             # Full-screen MJPEG + WS stats
│   ├── events.html           # Historical event log
│   ├── alerts.html           # Snapshot gallery
│   ├── evidence.html         # Encrypted evidence vault
│   ├── dispatch.html         # Emergency dispatch packages
│   └── authorized.html       # Face enrollment management
│
├── static/
│   ├── css/style.css         # Design system
│   ├── js/app.js             # WebSocket client, dashboard + explainability logic
│   ├── sounds/               # Siren audio assets
│   └── authorized_faces/     # Enrolled face images (runtime)
│
├── models/
│   ├── tci_xgboost.json      # XGBoost fusion model
│   └── yolov8n.pt            # YOLO model (auto-downloaded by ultralytics)
│
└── Doc/
    ├── SENTRIX_MASTER_TECHNICAL_REPORT.md
    ├── FUTURE_TECHNICAL_ADVANCEMENTS.md
    └── [architecture audit documents]
```

---

## Quick Start

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
```

Edit `.env` with at minimum:
- `SENTRIX_PASSWORD` — dashboard login password
- `SESSION_SECRET` — generate with `python -c "import secrets; print(secrets.token_hex(32))"`
- `CAMERA_SOURCES` — webcam index (usually `0`) or RTSP URL

Optional:
- `ROBOFLOW_API_KEY` — enables cloud weapon/fire detection
- Twilio credentials — enables SMS + call alerts
- `EVIDENCE_AES_KEY` — makes encrypted evidence readable across restarts

### 4. Run the app
```bash
python app.py
```

Open the dashboard at **http://127.0.0.1:8000** and log in with your `SENTRIX_PASSWORD`.

> The database and tables are created automatically on first run. No separate `init_db` step is needed.

### 5. (Optional) Run the smoke test
```bash
python smoke_test.py
```

---

## Configuration Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `SENTRIX_PASSWORD` | ✅ | `admin` | Dashboard login password |
| `SESSION_SECRET` | Recommended | — | HMAC signing key for session tokens |
| `CAMERA_SOURCES` | ✅ | `0` | Comma-separated webcam index or RTSP URL |
| `PUBLIC_SERVER_URL` | — | `http://127.0.0.1:8000` | Base URL for snapshot links in alerts |
| `ROBOFLOW_API_KEY` | Optional | — | Enables cloud weapon/fire detection |
| `TWILIO_ACCOUNT_SID` | Optional | — | Twilio SMS/call alerts |
| `TWILIO_AUTH_TOKEN` | Optional | — | Twilio auth |
| `TWILIO_PHONE_NUMBER` | Optional | — | From number |
| `ALERT_PHONE_NUMBER` | Optional | — | Target number for alerts |
| `EVIDENCE_AES_KEY` | Optional | auto-random | Hex key for evidence encryption (min 32 chars) |
| `RETENTION_DAYS` | Optional | `30` | Auto-prune days for events/snapshots |
| `VOSK_MODEL_PATH` | Optional | `vosk-model` | Path to VOSK model directory |
| `SENTRIX_USER_NAME` | Optional | `Unknown User` | Used in dispatch packages |
| `SENTRIX_USER_ADDRESS` | Optional | — | Used in dispatch packages |
| `SENTRIX_USER_PHONE` | Optional | — | Used in dispatch packages |
| `SENTRIX_CAMERA_LOCATION` | Optional | `Main Entrance` | Used in dispatch packages |

---

## TCI Threat Levels

| Level | Status | TCI Range | Actions |
|---|---|---|---|
| 1 | NORMAL | 0.00–0.25 | Log only |
| 2 | SUSPICIOUS | 0.26–0.50 | Snapshot + SMS |
| 3 | ELEVATED | 0.51–0.70 | + Siren + Encrypted evidence |
| 4 | HIGH | 0.71–0.85 | + Dispatch package pre-populated |
| 5 | CRITICAL | 0.86–1.00 | + Automated voice call |

**Hard overrides** (bypass fusion): fire ≥ 0.70 → Level 5 immediately; weapon ≥ 0.70 → Level 5; weapon ≥ 0.50 → Level 4.

---

## Security Posture

- **Authentication**: All pages, API endpoints, WebSocket, and MJPEG stream require a valid HMAC-SHA256 session token (12h expiry)
- **Session storage**: Tokens stored in `httponly` cookies — JavaScript cannot read them
- **Password safety**: Raw password never stored in cookie; HMAC signing key derived via PBKDF2
- **Upload safety**: Extension + MIME type validation, path-traversal-safe filename sanitization, 10MB size cap
- **Evidence integrity**: AES-256-GCM encryption with HKDF-derived stable key; SHA-256 tamper detection hash
- **Graceful shutdown**: Ctrl+C cleanly drains the task queue and releases camera handles

---

## Documentation

- [SENTRIX_MASTER_TECHNICAL_REPORT.md](Doc/SENTRIX_MASTER_TECHNICAL_REPORT.md)
- [FUTURE_TECHNICAL_ADVANCEMENTS.md](Doc/FUTURE_TECHNICAL_ADVANCEMENTS.md)
- [Doc/COMPLETE_ARCHITECTURE_MAP.md](Doc/COMPLETE_ARCHITECTURE_MAP.md)
- [Doc/SECURITY_AUDIT.md](Doc/SECURITY_AUDIT.md)
- [Doc/AI_PIPELINE_ANALYSIS.md](Doc/AI_PIPELINE_ANALYSIS.md)

---

## Security Notice

SENTRIX is designed for research and capstone use. Before production deployment, also consider: HTTPS/TLS termination, rate limiting, CSRF tokens on POST routes, log aggregation, and formal penetration testing.
