# System Design Document

## Project Name: MindLens

---

## 1. System Overview
MindLens is architected as a lightweight, decoupled client-server web application designed for high responsiveness, rapid iteration, and demonstrability within a 3-hour hackathon timeframe.

The system takes three user inputs (Decision, Context, and Reasoning), validates them on the client and server, processes them through an AI Reasoning Engine using a carefully engineered prompt with strict JSON schema constraints, and returns a structured diagnostic report rendered on a modern React interface.

---

## 2. Main Components
1. **React Frontend (Vite + JS):** Client single-page application providing input intake, client validation, dynamic loading indicators, and structured audit presentation.
2. **FastAPI Backend (Python):** High-performance asynchronous REST API handling payload validation, prompt assembly, secure LLM provider communication, response parsing, and optional database persistence.
3. **AI Reasoning Engine (LLM Provider API):** Large Language Model accessed via REST API executing the audit logic under strict system instructions and returning rigid JSON.
4. **PostgreSQL / Neon Database (Planned / Decoupled):** Cloud-hosted relational database for storing user accounts, decision logs, and audit histories.

---

## 3. Frontend Responsibilities
* **User Input Management:** Collect `decision`, `context`, and `reasoning` through clean, controlled form components.
* **Client-Side Validation:** Check for minimum length (e.g. reasoning >= 20 characters) and prevent empty submissions.
* **Asynchronous State Handling:** Manage `idle`, `loading` (with engaging auditing progress indicators), `success`, and `error` states.
* **Structured Rendering:** Render the 6 distinct audit categories into easily scannable visual cards with appropriate color accents and icons.
* **Authentication UI (Should-Have):** Simple modal or page for Login / Sign Up with JWT storage in `localStorage`.
* **Zero Secret Exposure:** Never hold, proxy, or reference LLM API keys directly in the frontend bundle.

---

## 4. Backend Responsibilities
* **CORS Middleware:** Permit secure cross-origin requests from the React development server and production domain.
* **Input Schema Validation:** Enforce data types and constraints via Pydantic models before triggering AI calls.
* **Prompt Assembly & Guardrails:** Construct the system and user prompts with explicit safety, cautious phrasing, and JSON schema constraints.
* **AI Provider Orchestration:** Send requests to the LLM API, handle network timeouts, and parse JSON responses safely with error fallback.
* **Authentication & Auth Middleware (Should-Have):** Issue and verify JWT access tokens; hash and verify passwords using `bcrypt`.
* **Persistence Layer (Should-Have):** Save decisions and audit reports to PostgreSQL via SQLAlchemy when a user is authenticated.

---

## 5. AI Engine Responsibilities
* **Audit, Not Arbitrate:** Never suggest the final choice; audit the internal logic and assumptions only.
* **Grounded Extraction:** Attribute every blind spot to the user's explicit statements or obvious contextual omissions.
* **Cautious Tone:** Express contradictions as "potential conflicts" or "possible tensions".
* **Structured Output Only:** Output pure, parseable JSON conforming strictly to the requested schema with no conversational fluff or markdown code fence leaks.

---

## 6. Database Responsibilities (Planned / Should-Have)
* **Users:** Store unique identity, email, and securely hashed passwords.
* **Decisions:** Store the raw decision text, context, and reasoning linked to a user.
* **Analyses:** Store the structured JSON audit output linked to the parent decision.
* *Note: The core AI audit endpoint functions independently even if the database is offline or unconfigured, preventing any database issue from blocking the MVP.*

---

## 7. Authentication Flow (Planned / Should-Have)
```
User
  │
  ▼
React (Login / Register Form)
  │  POST /api/auth/register or /api/auth/login
  ▼
FastAPI Auth Router
  │  1. Check user exists
  │  2. Verify bcrypt hash (or hash new password)
  │  3. Generate JWT access token with expiration
  ▼
FastAPI Response { access_token, token_type: "bearer", user }
  │
  ▼
React Client stores token in localStorage
  │  Subsequent requests include:
  │  Header: Authorization: Bearer <token>
  ▼
FastAPI Dependency (get_current_user) validates token
```

---

## 8. Decision Analysis Flow (Core Flow)

### Main Data Flow (Text / ASCII)
```
User
 │
 ▼
React Frontend (Vite)
 │ [Submits: { decision, context, reasoning }]
 ▼
FastAPI Backend (POST /api/audit)
 │
 ▼
Pydantic Validation (AuditRequest schema)
 │
 ▼
AI Reasoning Engine (Prompt Builder + LLM API)
 │ [Enforces: Grounding, Cautious Phrasing, Strict JSON Schema]
 ▼
Structured JSON Analysis
 │ [Blind spots, Assumptions, Verifications, Conflicts, Missing factors, Questions]
 ▼
FastAPI Response (HTTP 200 { status: "success", data: AnalysisResult })
 │
 ▼
React Result Page (Displays 6 Audit Cards)
```

### Database Persistence Flow (When Database is Active)
```
FastAPI Backend
 │
 ├──▶ Validate & Complete AI Audit
 │
 └──▶ (If User Authenticated)
        │
        ▼
      PostgreSQL / Neon
        ├── INSERT INTO decisions (user_id, decision, context, reasoning)
        └── INSERT INTO analyses (decision_id, blind_spots, assumptions, ...)
```

---

## 9. API Communication Flow
* **Protocol:** HTTP/1.1 REST over HTTPS.
* **Format:** `application/json` for all request and response bodies.
* **Core Endpoints:**
  * `POST /api/audit` - Core auditing endpoint (public or authenticated).
  * `POST /api/auth/register` - User registration (Should-Have).
  * `POST /api/auth/login` - User login (Should-Have).
  * `GET /api/history` - Retrieve previous audits for authenticated user (Should-Have).
  * `GET /api/health` - Basic health check endpoint returning server status.

---

## 10. Error Handling
* **Frontend:**
  * Displays user-friendly toast or banner if backend is unreachable.
  * Form field highlight if minimum input length is not met.
  * Timeout guard: notifies user if LLM call exceeds 20 seconds.
* **Backend:**
  * Pydantic validation error returns `422 Unprocessable Entity` with specific field issues.
  * LLM network/provider failure caught and returns `502 Bad Gateway` with clear error description.
  * Malformed LLM JSON caught with regex extraction fallback; if unrecoverable, returns a safe fallback structured error message instead of an unhandled `500`.

---

## 11. Security Considerations
* **API Key Protection:** LLM provider keys stored exclusively in backend `.env` file; zero exposure to frontend.
* **Password Hashing:** Passwords hashed with `bcrypt` (12 rounds) before storage; plaintext passwords never logged or saved.
* **CORS Restrictions:** Explicitly specify allowed origins; do not allow unrestricted wildcard credentials in production.
* **SQL Injection Prevention:** Use parameterized queries via SQLAlchemy ORM; no raw SQL string concatenation.
* **Input Sanitization:** Validate string length and structure to prevent oversized payloads or prompt injection attacks.

---

## 12. Deployment Architecture
* **Frontend Deployment:** Hosted on Vercel or Render Static Site (public working URL, fast global CDN).
* **Backend Deployment:** Hosted on Render, Railway, or Koyeb as a Python web service (running Uvicorn).
* **Database Deployment:** Neon Serverless PostgreSQL (free tier, instant provisioning, connection string via environment variable).
* **AI Provider:** External cloud API (Groq, OpenAI, or Google Gemini) authenticated via backend environment variable.
