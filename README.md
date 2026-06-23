Third Space Tracker (tentative claude generated readme)

A web app for finding, saving, and ranking "third spaces" — cafes, libraries, parks, coworking spots, and anywhere else you go to work, read, or socialize that isn't home or the office.


Problem

Moving to a new city and finding good spots is tedious. Search results are generic, reviews don't tell you what you actually want to know (is it quiet? good wifi? can you stay for 3 hours?), and there's no way to build a personal ranked list across different platforms.

Solution

Aggregate place data from free APIs, let users filter by what actually matters, and build a personal profile of saved and ranked spots.


Tech Stack

LayerChoiceWhyFrontendReact (Vite)Component-driven, good map library supportMappingLeaflet.js + OpenStreetMapCompletely free, no billing requiredBackendFastAPI (Python)Modern, async-friendly, auto-generates API docsDatabasePostgreSQL + PostGISNative geo queries (ST_DWithin, radius search)DB HostingSupabase (free tier)Managed Postgres, free, includes auth optionsBackend DeployRender (free tier)Simple deploys, free for personal projectsFrontend DeployVercelGenuinely free for personal projects

No credit card required for any of the above.


Data Sources

All free, no billing account needed:


Overpass API (OpenStreetMap) — primary source for cafes, libraries, parks, coworking spaces
Foursquare Places API — supplementary place data, 1,000 calls/day free
Yelp Fusion API — reviews and hours, 500 calls/day free



Architecture

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

The Places Aggregator is the core piece — it fans out to external APIs, deduplicates results (same cafe showing up in multiple sources), and normalizes everything into a consistent schema before storing or returning it.


Core Features (Planned)


 Search by location (lat/lng radius) with map and list views
 Filter by type (cafe, library, park, coworking, bar)
 Filter by amenities (wifi, noise level, hours, seating)
 Save spots to a personal profile
 Rate and add notes to saved spots
 Create named lists ("Focus spots", "Socialize", "Reading")
 User auth (register / login)



Data Model

sql-- Places discovered from external APIs
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


Project Structure (Planned)

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


Getting Started (Local Dev)

Prerequisites


Python 3.11+
Node 18+
PostgreSQL with PostGIS extension (or a Supabase project)


Backend

bashcd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up env vars
cp .env.example .env
# Fill in DATABASE_URL, FOURSQUARE_API_KEY, YELP_API_KEY

uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs

Frontend

bashcd frontend
npm install
npm run dev
# App at http://localhost:5173


API Keys Needed

ServiceWhere to getFree limitFoursquarefoursquare.com/developer1,000 req/dayYelpyelp.com/developers500 req/dayOverpassNo key neededRate limited by fair use


Build Order


FastAPI skeleton + DB connection + PostGIS setup
Overpass API integration — search cafes/libraries by lat/lng
React app + Leaflet map — display pins from API
Foursquare + Yelp integration + aggregator deduplication
Auth (register/login, JWT)
Save/unsave spots to profile
Personal ratings + notes
Filters (type, amenities, hours)
Lists feature
Deploy (Vercel + Render + Supabase)

Progress1 of 1Write README.md for Third Space TrackerThird space trackerInstructions · CLAUDE.mdREADME.mdContextTrack tools and referenced files used in this task.
