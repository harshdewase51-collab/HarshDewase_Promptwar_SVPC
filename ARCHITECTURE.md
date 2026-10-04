# Architecture Document

## Project Name: MindLens

---

## 1. High-Level Architecture
MindLens follows a modular, decoupled Client-Server architecture. The frontend is a lightweight Single Page Application (SPA) built with React and Vite, communicating via a REST API with a Python FastAPI backend. The FastAPI backend orchestrates prompt synthesis, LLM communication, validation, and optional database persistence with PostgreSQL / Neon.

```
┌───────────────────────────────────────────────────────────┐
│                     Client Tier                           │
│  React (Vite) Single Page Application                     │
│  - Input Forms (Decision, Context, Reasoning)             │
│  - Result Presentation Cards                              │
│  - Auth Context & API Service Layer                       │
└─────────────────────────────┬─────────────────────────────┘
                              │ HTTPS / REST (JSON)
┌─────────────────────────────▼─────────────────────────────┐
│                     Server Tier                           │
│  FastAPI (Python 3.10+)                                   │
│  ├── API Routers (/audit, /auth, /history)               │
│  ├── Pydantic Schemas (Input/Output validation)           │
│  ├── AI Service (Prompt builder, LLM client, JSON parser) │
│  └── Auth Service (JWT validation, bcrypt)                │
└──────────────┬─────────────────────────────┬──────────────┘
               │ Secure SDK / REST           │ SQLAlchemy
┌──────────────▼──────────────┐ ┌────────────▼──────────────┐
│       AI Provider Tier      │ │       Database Tier       │
│  LLM API (OpenAI / Groq /   │ │  PostgreSQL / Neon        │
│  Gemini)                    │ │  (Users, Decisions,       │
│  - Structured JSON audit    │ │   Analyses)               │
└─────────────────────────────┘ └───────────────────────────┘
```

---

## 2. Frontend Folder Structure
```
frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx                 # App entry point and root mounting
    ├── App.jsx                  # Main router and global layout
    ├── index.css                # Design tokens, typography, and utility classes
    ├── components/              # Reusable presentation and UI elements
    │   ├── Navbar.jsx           # Top navigation bar with branding & status
    │   ├── DecisionForm.jsx     # Triple-input form (Decision, Context, Reasoning)
    │   ├── AuditResult.jsx      # Result container displaying the 6 categories
    │   ├── AuditCard.jsx        # Individual styled card for category findings
    │   ├── LoadingState.jsx     # Auditing animation and progress indicator
    │   └── AuthModal.jsx        # Simple login/register dialog (Should-Have)
    ├── pages/                   # Top-level screen views
    │   ├── Home.jsx             # Primary workspace (Form + Results)
    │   ├── Dashboard.jsx        # Saved history and past decisions (Should-Have)
    │   └── About.jsx            # Philosophy, ethical rules, and guide
    ├── services/                # External communication and API clients
    │   └── api.js               # Centralized fetch/axios functions for backend
    ├── context/                 # Application-wide state providers
    │   └── AuthContext.jsx      # Authentication and active user state (Should-Have)
    └── utils/                   # Helper functions
        ├── constants.js         # Sample prompts, category labels, UI constants
        └── formatters.js        # Date and text formatting utilities
```

### Folder Responsibilities:
* `components/`: Pure and stateful visual UI components. Kept modular and focused.
* `pages/`: High-level views wired to routes or main screen toggles.
* `services/`: Encapsulates all network HTTP requests to the FastAPI backend. No component calls `fetch` directly.
* `context/`: React context for managing user authentication tokens and profile state across components.
* `utils/`: Reusable pure helper functions and standard constants.

---

## 3. Backend Folder Structure
```
backend/
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables blueprint
└── app/
    ├── main.py                  # FastAPI initialization, CORS, and router registry
    ├── routes/                  # API route controllers
    │   ├── audit.py             # POST /api/audit (Core audit endpoint)
    │   ├── auth.py              # POST /api/auth/login, /register (Should-Have)
    │   └── history.py           # GET /api/history (Should-Have)
    ├── services/                # Core business logic and external integrations
    │   ├── ai_service.py        # LLM client, prompt builder, JSON parsing
    │   └── prompt_template.py   # Grounded auditing system prompts
    ├── models/                  # SQLAlchemy ORM database models (Should-Have)
    │   ├── user.py              # User model
    │   ├── decision.py          # Decision model
    │   └── analysis.py          # Analysis model
    ├── schemas/                 # Pydantic schemas for request/response validation
    │   ├── audit.py             # AuditRequest and AuditResponse models
    │   └── auth.py              # UserCreate, UserLogin, Token models
    ├── database/                # Database connection and session management
    │   ├── session.py           # Engine creation and session maker
    │   └── base.py              # Base declarative model
    ├── auth/                    # Security, hashing, and token logic
    │   ├── security.py          # bcrypt password hashing and verification
    │   └── jwt.py               # JWT creation, decoding, and FastAPI dependencies
    └── utils/                   # Shared utility helpers
        └── logger.py            # Simple standardized console logging
```

### Folder Responsibilities:
* `routes/`: Handles incoming HTTP requests, validates via Pydantic, and delegates to services.
* `services/`: Houses core business logic, including prompt engineering and LLM API calls.
* `models/`: Defines PostgreSQL relational tables using SQLAlchemy ORM.
* `schemas/`: Defines type contracts, serialization rules, and input validations using Pydantic.
* `database/`: Manages database connections, engine lifecycle, and transactional sessions.
* `auth/`: Encapsulates password hashing and token validation logic.
* `utils/`: Standardized logging and error utilities.

---

## 4. Database Layer (Planned / Should-Have)
* **ORM:** SQLAlchemy 2.0.
* **Driver:** `asyncpg` or `psycopg2-binary`.
* **Engine Configuration:** Session pooling with `pool_pre_ping=True` for reliable cloud connection handling (e.g. Neon serverless suspension).
* **Decoupling Strategy:** All database calls inside `routes/audit.py` are wrapped in non-blocking try-except blocks. If the database is unconfigured or fails, the core AI audit response is still delivered to the user immediately.

---

## 5. AI Service Layer
* **Module:** `app/services/ai_service.py`
* **Responsibilities:**
  1. Constructs the system prompt containing the "Auditor, Not Decision-Maker" persona and safety guidelines.
  2. Constructs the user prompt merging `decision`, `context`, and `reasoning`.
  3. Invokes the LLM API using temperature `0.3`–`0.5` for balanced analytical precision and creative blind spot identification.
  4. Enforces JSON output format (`response_format={"type": "json_object"}` where supported).
  5. Parses the raw response string, handles edge cases (such as markdown code block backticks), and maps the data to the Pydantic `AuditResponse` schema.

---

## 6. Authentication Layer (Planned / Should-Have)
* **Standard:** OAuth2 Password Bearer pattern with JSON Web Tokens (JWT).
* **Algorithm:** HS256 with secret key loaded from environment variables.
* **Token Expiration:** 7 days standard validity for hackathon simplicity.
* **Security Helper:** Passlib with `bcrypt` algorithm.
* **FastAPI Dependency:** `get_current_user` extracts and verifies the bearer token from the `Authorization` header.

---

## 7. API Layer & Endpoint Specifications
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/audit` | Audits decision, context, and reasoning | Optional |
| `POST` | `/api/auth/register` | Creates a new user account | No |
| `POST` | `/api/auth/login` | Authenticates user and returns JWT token | No |
| `GET` | `/api/history` | Fetches previous decision audits for user | Yes |
| `GET` | `/api/health` | Returns backend operational status | No |

---

## 8. Data Flow
1. **User Input:** User enters data in `DecisionForm.jsx`.
2. **Client Dispatch:** `api.js` makes `POST /api/audit` request with JSON payload:
   ```json
   {
     "decision": "Accept a 6-month unpaid internship",
     "context": "Final year CS student with 3 courses left",
     "reasoning": "It will guarantee a job offer and looks prestigious on LinkedIn."
   }
   ```
3. **Server Ingestion:** `routes/audit.py` receives and validates the payload via `AuditRequest` Pydantic schema.
4. **AI Generation:** `ai_service.py` formats prompt and calls the LLM provider API.
5. **JSON Parsing & Validation:** Raw response is sanitized, parsed into JSON, and validated against `AuditResponse` schema.
6. **Optional Persistence:** If an authenticated user token is present, records are written to `decisions` and `analyses` tables.
7. **Client Rendering:** JSON response is returned to React; `AuditResult.jsx` renders the 6 categorized cards.

---

## 9. Error Flow
```
User Action
  │
  ├── Frontend Validation Fails ──▶ Display inline red warning (No network request)
  │
  └── Request Sent to Backend
        │
        ├── Pydantic Validation Fails ────▶ 422 Unprocessable Entity
        │                                  Frontend displays: "Please provide more details."
        │
        ├── LLM API Error / Timeout ──────▶ 502 Bad Gateway
        │                                  Frontend displays: "AI service busy. Please retry."
        │
        ├── LLM JSON Parsing Fails ───────▶ Fallback parser executes; if unresolvable, returns 500
        │                                  Frontend displays: "Unable to parse audit. Please retry."
        │
        └── Success ──────────────────────▶ 200 OK with clean structured JSON
```

---

## 10. Environment Variables

### Backend (`backend/.env`)
```bash
# Server Configuration
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app

# AI Provider Configuration
LLM_API_KEY=your_llm_api_key_here
LLM_MODEL=llama-3.3-70b-versatile # or gpt-4o-mini / gemini-1.5-flash
LLM_PROVIDER=groq # or openai / gemini

# Database Configuration (Planned / Should-Have)
DATABASE_URL=postgresql://user:password@ep-sample.us-east-2.aws.neon.tech/mindlens?sslmode=require

# Authentication Secrets (Planned / Should-Have)
JWT_SECRET=super_secret_jwt_key_change_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (`frontend/.env`)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

---

## 11. Deployment Structure
* **Frontend:** Vercel / Netlify
  * Build command: `npm run build`
  * Output directory: `dist`
  * Environment variable: `VITE_API_BASE_URL=https://your-backend.onrender.com`
* **Backend:** Render / Railway / Koyeb
  * Build command: `pip install -r requirements.txt`
  * Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
* **Database:** Neon PostgreSQL (Cloud Serverless)
  * Managed connection string with SSL mode enabled.
