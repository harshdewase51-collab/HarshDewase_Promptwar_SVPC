# MindLens 🧠🔍

> **“MindLens doesn't tell you what decision to make; it tells you what you might be missing before you make it.”**

MindLens is an objective, non-prescriptive AI reasoning auditor built for the hackathon challenge *"The Blind Spot"*. Instead of telling users what choice to make, MindLens audits the user's *own logic*, uncovering unexamined assumptions, evidence-grounded blind spots, and hidden tensions before high-stakes choices are locked in.

---

## 📌 Problem
When faced with significant life, career, or academic choices, humans naturally fall victim to confirmation bias and tunnel vision. People often rationalize a decision around one or two attractive perks (e.g., high pay or prestige) while remaining blind to unspoken premises, personal trade-offs, and critical gaps in their reasoning.

Traditional conversational AI tools make this worse: they act as sycophants (validating whatever the user says) or pretend to be omniscient authorities dictating what the user *should* do.

## 💡 Solution
MindLens audits the reasoning behind the decision without stealing the user's agency.

By taking three simple inputs:
1. **The Decision:** What choice is being considered?
2. **The Context:** What is the background situation, timeline, and stakes?
3. **The Reasoning:** Why does the user believe this is the right choice?

MindLens's Reasoning Engine breaks down the argument into structured, evidence-grounded insights, presenting the user with concrete questions and verification steps to explore.

---

## 🌟 Why MindLens is Different
Most AI tools try to be decision-makers. MindLens is a **reasoning auditor**.

* 🔍 **Evidence-Linked Blind Spots:** Every flagged blind spot is tied directly to what the user wrote or explicitly omitted.
* 💡 **Assumption → Verification:** Hidden premises are not just flagged; the user is given concrete, real-world steps to verify them.
* ⚖️ **Potential Conflict Detection:** Inconsistencies between stated goals and the chosen path are presented respectfully using cautious language (*"potential conflict"*, *"possible tension"*).
* 🧩 **Context-Specific Missing Factors:** Surfaces overlooked operational dimensions (e.g., burnout risk, mentor availability, academic rules).
* ❓ **Actionable Critical Questions:** Prompts self-reflection rather than delivering generic advice.

*(Note: MindLens does not claim to eliminate risk or predict the future. It is a structured tool for rigorous self-reflection.)*

---

## ✨ Features

### Core MVP (Must-Have)
- [ ] **Triple-Input Intake:** Dedicated fields for Decision, Context, and Reasoning.
- [ ] **One-Click Dilemma Demo:** Preload standard dilemmas (e.g., "The 6-Month Internship Dilemma") for instant demonstration.
- [ ] **AI Reasoning Engine:** FastAPI backend integrating LLM API with strict system instructions.
- [ ] **Structured 6-Category Output:** Guaranteed JSON schema covering blind spots, assumptions, verifications, tensions, missing factors, and critical questions.
- [ ] **Card-Based Result Presentation:** Visual cards with color coding and distinct iconography.

### Planned Enhancements (Should-Have / Future)
- [ ] **User Authentication:** Optional JWT + bcrypt user accounts.
- [ ] **Audit History:** Database persistence (PostgreSQL / Neon) to track past decisions over time.
- [ ] **Personal Dashboard:** Archive view of previously audited reasoning.
- [ ] **Reflection Loop:** Re-run analysis after revising your reasoning based on findings.
- [ ] **Export Options:** Download audit summaries as Markdown or PDF.

---

## 🛠️ Tech Stack

* **Frontend:** React (Vite), JavaScript, Vanilla Modern CSS
* **Backend:** Python, FastAPI, Pydantic, Uvicorn
* **AI Provider:** LLM API (Groq / OpenAI / Google Gemini)
* **Database (Planned):** PostgreSQL / Neon Serverless (SQLAlchemy ORM)
* **Authentication (Planned):** JWT (JSON Web Tokens), `passlib[bcrypt]`
* **API Style:** REST (JSON)
* **Deployment Target:** Frontend on Vercel; Backend on Render / Railway

---

## 🏛️ Architecture Overview

```
User (Browser)
      │
      ▼
React Frontend (Vite)
      │  HTTP POST /api/audit { decision, context, reasoning }
      ▼
FastAPI Backend
      ├── Pydantic Input Validation
      ├── Grounded Prompt Assembly
      ▼
AI Reasoning Engine (LLM API)
      │  Structured JSON Response
      ▼
FastAPI Output Validation
      │  HTTP 200 { status: "success", data: AnalysisResult }
      ▼
React Result Interface (6 Categorized Audit Cards)
```

---

## 📋 The 6 AI Analysis Categories

1. **Evidence-Linked Blind Spots:** Unconsidered realities directly tied to statements made by the user.
2. **Hidden Assumptions:** Unstated beliefs the user is treating as established facts.
3. **Assumption Verification:** Tangible questions or actions to test those assumptions before deciding.
4. **Potential Conflicts / Tensions:** Cautiously identified frictions between stated priorities and chosen logic.
5. **Missing Factors:** Crucial situational dimensions (health, finances, long-term options) left unaddressed.
6. **Critical Questions:** High-impact reflection prompts to help the user clarify their own judgment.

---

## 🚀 Getting Started Locally

### Prerequisites
* **Node.js** (v18+)
* **Python** (v3.10+)
* An API key for an LLM provider (Groq, OpenAI, or Gemini)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/MindLens.git
cd MindLens
```

### 2. Backend Setup
```bash
cd backend
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and insert your LLM_API_KEY

# Start backend dev server
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000`.  
Interactive API docs available at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Frontend will be live at `http://localhost:5173`.

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)
```bash
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173

# AI Credentials
LLM_API_KEY=your_actual_api_key_here
LLM_MODEL=llama-3.3-70b-versatile
LLM_PROVIDER=groq

# Database (Planned / Optional for MVP)
DATABASE_URL=postgresql://user:password@ep-sample.us-east-2.aws.neon.tech/mindlens?sslmode=require

# Authentication (Planned / Optional for MVP)
JWT_SECRET=super_secret_dev_key
```

### Frontend (`frontend/.env`)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🔌 API Overview

### `POST /api/audit`
Audits the user's decision reasoning. Publicly accessible for core MVP.

**Request Body:**
```json
{
  "decision": "Accept a 6-month startup internship instead of finishing college on schedule.",
  "context": "Senior CS student with 2 semesters left; startup has 4 engineers; stipend is $3500/mo.",
  "reasoning": "The pay is great and startup experience will guarantee higher-paying job offers later."
}
```

**Response Body (HTTP 200):**
```json
{
  "status": "success",
  "data": {
    "blind_spots": [
      {
        "point": "Mentorship bandwidth at a 4-engineer startup.",
        "evidence": "You noted a 4-engineer team, but have not confirmed whether engineers have time to mentor."
      }
    ],
    "assumptions": [
      {
        "assumption": "Startup experience guarantees higher offers regardless of graduation date.",
        "verification": "Check with recent graduates or recruiters to verify how a delayed degree is perceived."
      }
    ],
    "conflicts": [
      {
        "tension": "Potential tension between career acceleration and university graduation requirements.",
        "explanation": "You noted having 2 semesters remaining, but have not verified university leave-of-absence rules."
      }
    ],
    "missing_factors": [
      "Loss of academic momentum and scholarship eligibility.",
      "Workplace expectations and potential burnout at an early-stage startup."
    ],
    "critical_questions": [
      "If the startup does not provide a return offer, what is your contingency plan to finish your degree?",
      "Have you spoken directly with past interns from this company?"
    ]
  }
}
```

---

## 🛡️ Trust & Safety Rules
* **No Prescriptive Advice:** MindLens will never tell you what decision to make.
* **Grounded Findings:** All observations stem strictly from the user's input.
* **Respectful Language:** Potential contradictions are framed cautiously (*"possible tension"*, *"you may want to examine"*).
* **No Psychological Profiling:** Focuses purely on logic and reasoning gaps.

---

## 📊 Project Status
* **Documentation:** `COMPLETED`
* **Core Application Code:** `NOT IMPLEMENTED` (Pending Phase 1 scaffolding)
* **AI Integration:** `NOT IMPLEMENTED` (Planned Phase 4)
* **Database & Auth:** `PLANNED / NOT IMPLEMENTED YET` (Phase 2 & 7)

---

## 🔮 Future Improvements
* Multi-option comparison matrix (Side-by-side audit of Option A vs. Option B).
* Team reasoning audit for collaborative decision-making.
* Follow-up reflection tracker to measure decision outcomes over 3–6 months.
