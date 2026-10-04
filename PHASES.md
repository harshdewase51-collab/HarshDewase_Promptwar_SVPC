# Implementation Phases

## Project Name: MindLens

---

> [!IMPORTANT]
> **Execution Strategy:**
> - Each phase must be completed, tested, and verified before advancing to the next.
> - **Time Budget:** ~3 Hours total.
> - **Fallback Priority:** If time becomes constrained, prioritize **Core AI Flow → Result Page → Deployment** over Authentication and Database History.

```
PRIORITY ORDER IF TIME SHORTENS:
1. Core Decision Flow (Phases 1, 3)
2. AI Analysis Engine (Phase 4)
3. MindLens Uniqueness (Audit Depth) (Phase 5)
4. Result Page (Phase 6)
5. Public Deployment (Phase 10)
6. Authentication (Phase 2)
7. Database / Save & History (Phase 7)
8. Dashboard (Phase 8)
9. Testing Polish (Phase 9)
10. Bonus Features (Phase 11)
```

---

## PHASE 0 — Existing Project Check
* **Estimated Time:** 5 min
* **Status:** `COMPLETED` (Verified clean empty workspace in `D:\MindLens`)
* **Goal:** Inspect directory structure, verify existing files/tools, and ensure no clashing setups exist.
* **What Will Be Built / Done:**
  * Verify Node.js, Python, and package managers exist on system.
  * Audit active workspace directory for existing code or conflicting templates.
* **Files Affected:** N/A (Inspection only).
* **Dependencies:** None.
* **Testing:** Run `node -v` and `python --version` in terminal.
* **Expected Output:** Confirmation of clean workspace ready for project scaffolding.

---

## PHASE 1 — Project Foundation
* **Estimated Time:** 10 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Establish the decoupled frontend and backend project structure with baseline dependencies and environment configuration.
* **What Will Be Built:**
  * Scaffold React + Vite frontend (`frontend/`).
  * Scaffold FastAPI Python project structure (`backend/` with `app/main.py`, `requirements.txt`).
  * Set up CORS middleware in FastAPI to allow frontend communication.
  * Setup `.env.example` and `.gitignore`.
* **Files Affected:**
  * `frontend/package.json`
  * `frontend/vite.config.js`
  * `frontend/src/App.jsx`
  * `frontend/src/index.css`
  * `backend/requirements.txt`
  * `backend/app/main.py`
  * `backend/.env.example`
* **Dependencies:**
  * Frontend: `react`, `react-dom`
  * Backend: `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`
* **Testing:**
  * Run backend: `uvicorn app.main:app --reload` -> visit `http://localhost:8000/api/health` -> returns `{"status": "ok"}`.
  * Run frontend: `npm run dev` -> loads starter page at `http://localhost:5173`.
* **Expected Output:** Clean running frontend and backend communicating successfully.

---

## PHASE 2 — Authentication (Should-Have / Decoupled)
* **Estimated Time:** 15 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Create simple user registration, login, and JWT token issuance (designed to be optional so it does not block the core flow).
* **What Will Be Built:**
  * Backend JWT token generator and password hashing utility using `passlib[bcrypt]`.
  * `POST /api/auth/register` and `POST /api/auth/login` endpoints.
  * Frontend `AuthContext` to store JWT in `localStorage` and expose `user` state.
  * Simple modal or toggle for Login/Signup.
* **Files Affected:**
  * `backend/app/auth/security.py`
  * `backend/app/auth/jwt.py`
  * `backend/app/routes/auth.py`
  * `backend/app/schemas/auth.py`
  * `frontend/src/context/AuthContext.jsx`
  * `frontend/src/components/AuthModal.jsx`
* **Dependencies:** `passlib[bcrypt]`, `python-jose` (or `PyJWT`).
* **Testing:**
  * Test `POST /api/auth/register` via Swagger docs (`/docs`).
  * Test `POST /api/auth/login` -> receive valid bearer token.
* **Expected Output:** User can register, log in, and store their token in the browser.

---

## PHASE 3 — Decision Input
* **Estimated Time:** 15 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Build an intuitive, guided triple-input interface (Decision, Context, Reasoning) with validation.
* **What Will Be Built:**
  * `DecisionForm.jsx` containing:
    1. Decision field: "What choice are you considering?"
    2. Context field: "What is your background, timeline, constraints?"
    3. Reasoning field: "Why do you think this is the right decision?"
  * Quick-fill example button (e.g., "Load Student Internship Dilemma") for rapid demoing.
  * Validation rules (minimum character threshold for reasoning).
  * API service client (`services/api.js`) for firing the audit request.
* **Files Affected:**
  * `frontend/src/components/DecisionForm.jsx`
  * `frontend/src/services/api.js`
  * `frontend/src/utils/constants.js`
  * `frontend/src/index.css`
* **Dependencies:** None (Standard React state and CSS).
* **Testing:** Click "Load Example" -> form populates; submit empty form -> shows validation warning; submit valid form -> triggers API call.
* **Expected Output:** Responsive, polished input form with user guidance and quick-fill capability.

---

## PHASE 4 — AI Reasoning Engine
* **Estimated Time:** 30 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Implement the FastAPI reasoning pipeline with prompt engineering, LLM API integration, and strict JSON output parsing.
* **What Will Be Built:**
  * Prompt engineering template enforcing the "Auditor, Not Decision-Maker" persona.
  * `ai_service.py` integrating LLM API (Groq/OpenAI/Gemini).
  * Backend `POST /api/audit` route with `AuditRequest` and `AuditResponse` Pydantic models.
  * Robust JSON parser with fallback sanitization to guarantee valid parsing.
* **Files Affected:**
  * `backend/app/services/prompt_template.py`
  * `backend/app/services/ai_service.py`
  * `backend/app/routes/audit.py`
  * `backend/app/schemas/audit.py`
* **Dependencies:** `httpx` or official SDK (`groq`, `openai`, or `google-generativeai`).
* **Testing:**
  * Send sample payload via `curl` or Swagger UI to `/api/audit`.
  * Validate that returned response contains all 6 JSON keys with valid grounded content.
* **Expected Output:** Backend receives user inputs, calls LLM, and returns structured audit JSON in < 15 seconds.

---

## PHASE 5 — MindLens Uniqueness (Audit Depth)
* **Estimated Time:** 20 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Ensure the AI output strictly adheres to the unique value proposition: evidence-linked blind spots, assumption-verification pairs, cautious conflict language, and missing dimensions.
* **What Will Be Built:**
  * Refined few-shot prompt instructions ensuring:
    * Blind spots cite user evidence.
    * Every assumption includes a tangible verification question/step.
    * Conflicts use cautious language ("potential tension", "possible conflict").
    * Contextual omissions represent non-obvious angles (e.g. burnout, opportunity cost, long-term options).
  * Output schema validator ensuring no generic or hollow responses.
* **Files Affected:**
  * `backend/app/services/prompt_template.py`
  * `backend/app/services/ai_service.py`
* **Dependencies:** None.
* **Testing:** Test with 3 distinct decision domains (Career/Internship, Financial/Purchase, Personal/Relocation) to confirm high relevance and adherence to trust rules.
* **Expected Output:** Highly differentiated, non-sycophantic audit outputs that impress evaluators.

---

## PHASE 6 — Result Page
* **Estimated Time:** 15 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Build a visually stunning, readable presentation interface for the 6 audit dimensions.
* **What Will Be Built:**
  * `AuditResult.jsx` container rendering distinct sections.
  * `AuditCard.jsx` with distinct color accents, badges, and icon indicators:
    * 🔍 Evidence-Linked Blind Spots (Amber/Warning accent)
    * 💡 Hidden Assumptions & Verifications (Blue/Insight accent)
    * ⚖️ Potential Conflicts / Tensions (Purple/Balance accent)
    * 🧩 Context Missing Factors (Teal/Dimension accent)
    * ❓ Critical Questions to Consider (Indigo/Reflection accent)
  * Dynamic loading animation (`LoadingState.jsx`) displaying rotating audit steps ("Auditing assumptions...", "Scanning for missing factors...").
  * Action buttons: "Edit Reasoning", "Copy Audit", "New Decision".
* **Files Affected:**
  * `frontend/src/components/AuditResult.jsx`
  * `frontend/src/components/AuditCard.jsx`
  * `frontend/src/components/LoadingState.jsx`
  * `frontend/src/index.css`
* **Dependencies:** None (Pure CSS & SVGs).
* **Testing:** Submit a test decision -> verify smooth transition to loading state -> verify rendered cards are readable and responsive.
* **Expected Output:** Professional, accessible dashboard-style audit results.

---

## PHASE 7 — Save + History (Should-Have)
* **Estimated Time:** 15 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Integrate PostgreSQL / Neon persistence for saving decisions and viewing past audits.
* **What Will Be Built:**
  * SQLAlchemy models for `users`, `decisions`, and `analyses`.
  * Database connection utility in `backend/app/database/session.py`.
  * Automatic persistence logic inside `POST /api/audit` when user token is present.
  * `GET /api/history` endpoint to return past decisions for current user.
* **Files Affected:**
  * `backend/app/models/user.py`
  * `backend/app/models/decision.py`
  * `backend/app/models/analysis.py`
  * `backend/app/database/session.py`
  * `backend/app/routes/history.py`
* **Dependencies:** `sqlalchemy`, `asyncpg` or `psycopg2-binary`.
* **Testing:** Perform an audit while logged in -> query `/api/history` -> verify audit appears in returned list.
* **Expected Output:** Authenticated decisions automatically saved and retrievable.

---

## PHASE 8 — Dashboard (Should-Have)
* **Estimated Time:** 10 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Build a simple personal dashboard page where users can browse their previous decision audits.
* **What Will Be Built:**
  * `Dashboard.jsx` page displaying a chronological list of audited decisions.
  * Ability to click an old decision to reload its full 6-card audit view.
  * Empty state with call-to-action to "Audit your first decision".
* **Files Affected:**
  * `frontend/src/pages/Dashboard.jsx`
  * `frontend/src/components/HistoryItem.jsx`
* **Dependencies:** None.
* **Testing:** Navigate to `/dashboard` -> view saved decisions -> click to inspect details.
* **Expected Output:** Clean, intuitive personal decision audit archive.

---

## PHASE 9 — Testing & Edge Case Polish
* **Estimated Time:** 15 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Rigorous end-to-end testing, error handling verification, and demo rehearsals.
* **What Will Be Built / Executed:**
  * Test edge cases: very short input, long input, edge characters, rapid double clicks.
  * Verify API timeout handling and user-facing error toasts.
  * Rehearse the standard Hackathon Demo Dilemma ("The 6-Month Internship Dilemma").
  * Verify mobile responsiveness and layout adaptability.
* **Files Affected:** Bug fixes across frontend components and backend handlers.
* **Dependencies:** None.
* **Testing:** Perform full cycle test without errors.
* **Expected Output:** Zero unhandled errors; bulletproof demo flow.

---

## PHASE 10 — Public Deployment
* **Estimated Time:** 15 min
* **Status:** `NOT IMPLEMENTED`
* **Goal:** Deploy the application to production with a publicly accessible, working URL.
* **What Will Be Built / Configured:**
  * Deploy backend to Render, Railway, or Koyeb (ensure `LLM_API_KEY` and `CORS_ORIGINS` configured).
  * Deploy frontend to Vercel or Render Static Sites (configure `VITE_API_BASE_URL`).
  * Verify SSL certificate and HTTPS connectivity between client and server.
* **Files Affected:**
  * `vercel.json` or `render.yaml`
  * Deployment environment variables.
* **Dependencies:** Git repository connection.
* **Testing:** Open public frontend URL on a separate device (e.g. mobile phone), submit an audit, verify successful real-time result.
* **Expected Output:** Fully operational public URL ready for hackathon submission and judging.

---

## PHASE 11 — Bonus Features (Only If Time Remains)
* **Estimated Time:** Variable (Remaining time)
* **Status:** `NOT IMPLEMENTED`
* **Potential Enhancements:**
  1. **Reflection Loop:** "Revise my reasoning" button allowing the user to type updated thoughts and see how blind spots change.
  2. **PDF/Markdown Export:** One-click download of the complete audit report.
  3. **Voice Input:** Web Speech API button allowing the user to dictate their dilemma.
  4. **Micro-Interactions:** Subtle card reveal animations and smooth transitions.
