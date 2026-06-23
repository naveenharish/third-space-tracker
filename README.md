# Third Space Tracker (tentative claude generated)

A web app for finding, saving, and ranking "third spaces" — cafes, libraries, parks, coworking spots, and anywhere else you go to work, read, or socialize that isn't home or the office.

---

## Problem

Moving to a new city and finding good spots is tedious. Search results are generic, reviews don't tell you what you actually want to know (is it quiet? good wifi? can you stay for 3 hours?), and there's no way to build a personal ranked list across different platforms.

## Solution

Aggregate place data from free APIs, let users filter by what actually matters, and build a personal profile of saved and ranked spots.

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React (Vite) | Component-driven, good map library support |
| Mapping | Leaflet.js + OpenStreetMap | Completely free, no billing required |
| Backend | FastAPI (Python) | Modern, async-friendly, auto-generates API docs |
| Database | PostgreSQL + PostGIS | Native geo queries (`ST_DWithin`, radius search) |
| DB Hosting | Supabase (free tier) | Managed Postgres, free, includes auth options |
| Backend Deploy | Render (free tier) | Simple deploys, free for personal projects |
| Frontend Deploy | Vercel | Genuinely free for personal projects |

**No credit card required for any of the above.**

---

## Data Sources

All free, no billing account needed:

- **Overpass API** (OpenStreetMap) — primary source for cafes, libraries, parks, coworking spaces
- **Foursquare Places API** — supplementary place data, 1,000 calls/day free
- **Yelp Fusion API** — reviews and hours, 500 calls/day free

---

## Architecture

```
Browser
  ├── React App (Vite + React Router)
  ├── Map View (Leaflet + OSM tiles)
  └── Auth / Profile (JWT, saved spots)
        │
        ▼
   FastAPI (REST)
  ├── Places Aggregator ──► Overpass API
  │     normalize + dedupe ──► Foursquare API
  │                        ──► Yelp Fusion API
  └── PostgreSQL (PostGIS)
        └── Users, SavedPlaces, Ratings, Lists
```

The **Places Aggregator** is the core piece — it fans out to external APIs, deduplicates results (same cafe showing up in multiple sources), and normalizes everything into a consistent schema before storing or returning it.

---

## Core Features (Planned)

- [ ] Search by location (lat/lng radius) with map and list views
- [ ] Filter by type (cafe, library, park, coworking, bar)
- [ ] Filter by amenities (wifi, noise level, hours, seating)
- [ ] Save spots to a personal profile
- [ ] Rate and add notes to saved spots
- [ ] Create named lists ("Focus spots", "Socialize", "Reading")
- [ ] User auth (register / login)

---

## Data Model

```sql
-- Places discovered from external APIs
Place (
  id, name, type,
  lat, lng,           -- PostGIS POINT geometry
  source_ids,         -- { overpass: "...", foursquare: "...", yelp: "..." }
  amenities,          -- { wifi: true, noise: "quiet", ... }
  hours               -- JSON
)

-- User accounts
User (id, email, password_hash, created_at)

-- Personal saved spots
SavedPlace (
  id, user_id, place_id,
  personal_rating,    -- 1–5
  notes,              -- free text
  tags,               -- ["focus", "quiet", "good coffee"]
  saved_at
)

-- Named collections
List (id, user_id, name, place_ids)
```

---

## Project Structure (Planned)

```
third-space-tracker/
├── frontend/               # React (Vite)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/            # API client
│   └── package.json
│
├── backend/                # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── places.py   # Search + place detail
│   │   │   └── users.py    # Auth + saved spots
│   │   ├── aggregator/
│   │   │   ├── overpass.py
│   │   │   ├── foursquare.py
│   │   │   └── yelp.py
│   │   ├── models.py
│   │   └── database.py
│   └── requirements.txt
│
└── README.md
```

---

## Getting Started (Local Dev)

### Prerequisites

- Python 3.11+
- Node 18+
- PostgreSQL with PostGIS extension (or a Supabase project)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up env vars
cp .env.example .env
# Fill in DATABASE_URL, FOURSQUARE_API_KEY, YELP_API_KEY

uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# App at http://localhost:5173
```

---

## API Keys Needed

| Service | Where to get | Free limit |
|---|---|---|
| Foursquare | [foursquare.com/developer](https://foursquare.com/developer) | 1,000 req/day |
| Yelp | [yelp.com/developers](https://www.yelp.com/developers) | 500 req/day |
| Overpass | No key needed | Rate limited by fair use |

---

## Build Order

1. FastAPI skeleton + DB connection + PostGIS setup
2. Overpass API integration — search cafes/libraries by lat/lng
3. React app + Leaflet map — display pins from API
4. Foursquare + Yelp integration + aggregator deduplication
5. Auth (register/login, JWT)
6. Save/unsave spots to profile
7. Personal ratings + notes
8. Filters (type, amenities, hours)
9. Lists feature
10. Deploy (Vercel + Render + Supabase)
