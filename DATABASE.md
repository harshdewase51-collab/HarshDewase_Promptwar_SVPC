# Database Design Document

## Project Name: MindLens

---

> [!IMPORTANT]
> **Implementation Status: PLANNED / NOT IMPLEMENTED YET**  
> In accordance with the hackathon execution rules, the core AI audit workflow runs independently without requiring an active database connection. Database integration is scheduled for **Phase 7 & 8** (Should-Have scope) and will NOT block the core MVP.

---

## 1. Overview
The MindLens database is a lightweight, relational design tailored for PostgreSQL (specifically optimized for serverless instances like **Neon**). It maintains user identities, stores the raw decision submissions, and archives the resulting 6-category structured audits for historical tracking and review.

---

## 2. Table Specifications

### A. `users` Table
Stores registered user credentials and account metadata.
* **Why it exists:** Enables user ownership of decision histories and secures personal reflections behind authenticated sessions.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` (or `SERIAL`) | `PRIMARY KEY`, default `gen_random_uuid()` | Unique user identifier |
| `name` | `VARCHAR(100)` | `NOT NULL` | Display name of the user |
| `email` | `VARCHAR(255)` | `NOT NULL`, `UNIQUE` | User email address for authentication |
| `password_hash`| `VARCHAR(255)` | `NOT NULL` | bcrypt-hashed password (cost factor 12) |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, default `CURRENT_TIMESTAMP` | Account creation timestamp |

---

### B. `decisions` Table
Stores the user's primary decision dilemma, background context, and reasoning.
* **Why it exists:** Preserves the user's raw, unedited thoughts before auditing, establishing the baseline for analysis.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` (or `SERIAL`) | `PRIMARY KEY`, default `gen_random_uuid()` | Unique decision identifier |
| `user_id` | `UUID` | `FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE` | Owner user ID |
| `decision` | `TEXT` | `NOT NULL` | The specific decision being evaluated |
| `context` | `TEXT` | `NOT NULL` | Background situation, stakes, and constraints |
| `reasoning` | `TEXT` | `NOT NULL` | User's logic, rationale, and current belief |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, default `CURRENT_TIMESTAMP` | Timestamp of submission |

---

### C. `analyses` Table
Stores the 6-dimension AI audit output linked to a specific decision record.
* **Why it exists:** Caches the structured audit output so the user can revisit past reflections without incurring re-analysis latency or LLM token costs.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` (or `SERIAL`) | `PRIMARY KEY`, default `gen_random_uuid()` | Unique analysis identifier |
| `decision_id` | `UUID` | `FOREIGN KEY REFERENCES decisions(id) ON DELETE CASCADE` | Associated decision record |
| `blind_spots` | `JSONB` (or `TEXT`) | `NOT NULL` | Array of evidence-linked blind spots |
| `assumptions` | `JSONB` (or `TEXT`) | `NOT NULL` | Array of hidden assumptions with verification actions |
| `conflicts` | `JSONB` (or `TEXT`) | `NOT NULL` | Array of potential tensions or contradictions |
| `missing_factors` | `JSONB` (or `TEXT`) | `NOT NULL` | Array of context-specific omitted dimensions |
| `critical_questions` | `JSONB` (or `TEXT`) | `NOT NULL` | Array of thought-provoking reflection questions |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, default `CURRENT_TIMESTAMP` | Timestamp when audit was generated |

---

## 3. Relationships & Cardinality

```
┌──────────────────┐
│      users       │
│  (1 User)        │
└────────┬─────────┘
         │
         │ 1 : N (One user has many decisions)
         ▼
┌──────────────────┐
│    decisions     │
│  (N Decisions)   │
└────────┬─────────┘
         │
         │ 1 : 1 (or 1 : N for iterative re-audits)
         ▼
┌──────────────────┐
│     analyses     │
│  (1 Analysis)    │
└──────────────────┘
```

* **`users` to `decisions`:** One-to-Many (`1:N`). A single user can log multiple decision inquiries over time. If a user account is deleted, their decisions are deleted via `ON DELETE CASCADE`.
* **`decisions` to `analyses`:** One-to-One (`1:1`) for standard audits, expandable to One-to-Many (`1:N`) if reflection/re-audit loops are triggered. Deleting a decision record cascades to its audit findings.

---

## 4. Key Constraints & Design Rationale
1. **`JSONB` vs. Separate Tables for Findings:**
   * Using PostgreSQL `JSONB` for `blind_spots`, `assumptions`, etc., avoids unnecessary joins across 6 normalized micro-tables.
   * Enables storing structured metadata (e.g. `{ "assumption": "...", "verification": "..." }`) cleanly in a single record.
2. **`ON DELETE CASCADE`:** Ensures clean cascading removal of dependent records when parent records are dropped.
3. **Indices:**
   * Index on `users(email)` for fast login queries.
   * Index on `decisions(user_id)` for quick dashboard history retrieval.
   * Index on `analyses(decision_id)` for instantaneous lookup of saved audits.

---

## 5. PostgreSQL SQL Schema (DDL)

```sql
-- Enable UUID extension if using UUID primary keys
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Decisions Table
CREATE TABLE IF NOT EXISTS decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    decision TEXT NOT NULL,
    context TEXT NOT NULL,
    reasoning TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Analyses Table
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    decision_id UUID NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    blind_spots JSONB NOT NULL,
    assumptions JSONB NOT NULL,
    conflicts JSONB NOT NULL,
    missing_factors JSONB NOT NULL,
    critical_questions JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_decisions_user_id ON decisions(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_decision_id ON analyses(decision_id);
```

---

## 6. Example Records

### Example User Record:
```sql
INSERT INTO users (id, name, email, password_hash, created_at)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Alex Rivera',
    'alex@example.com',
    '$2b$12$e80yqXy1Fq1Z3a5Tj0K3eO1D8Z0y3t4R2l.5p9A8v7b6c5d4e3f2g', -- bcrypt hash
    NOW()
);
```

### Example Decision Record:
```sql
INSERT INTO decisions (id, user_id, decision, context, reasoning, created_at)
VALUES (
    'b1ffcd88-8b1a-4de7-aa5c-5aa8ac270b22',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Accept a 6-month internship at an early-stage startup instead of finishing college on schedule.',
    'Senior computer science student with 2 semesters remaining. Stipend is $3,500/month. The startup has 4 engineers.',
    'The stipend is great, and having real startup experience on my resume will guarantee higher-paying job offers later regardless of my graduation date.',
    NOW()
);
```

### Example Analysis Record:
```sql
INSERT INTO analyses (
    id,
    decision_id,
    blind_spots,
    assumptions,
    conflicts,
    missing_factors,
    critical_questions,
    created_at
)
VALUES (
    'c2eedc77-7c2b-4cd6-994b-4bb7ab160c33',
    'b1ffcd88-8b1a-4de7-aa5c-5aa8ac270b22',
    '[
        {
            "point": "Lack of structured mentorship at a 4-engineer startup",
            "evidence": "You mentioned the company has only 4 engineers, but your reasoning does not account for their bandwidth to mentor an intern."
        }
    ]'::jsonb,
    '[
        {
            "assumption": "Startup experience automatically guarantees higher-paying job offers.",
            "verification": "Talk to 2-3 recent graduates or hiring managers to verify whether delayed graduation impacted their offer rates."
        }
    ]'::jsonb,
    '[
        {
            "tension": "Potential tension between career acceleration and graduation requirements.",
            "explanation": "You noted having 2 semesters remaining, but have not detailed whether the university permits a leave of absence without re-enrollment penalties."
        }
    ]'::jsonb,
    '[
        "Academic standing and scholarship loss due to paused enrollment.",
        "Burnout risks associated with early-stage startup hours."
    ]'::jsonb,
    '[
        "If the startup does not extend a full-time return offer, what is your contingency plan for completing your degree?",
        "Have you verified the weekly hour expectation with the founders?"
    ]'::jsonb,
    NOW()
);
```

---

## 7. Migration & Local Development Strategy
* **Zero Initial Blocker:** For Phase 1–6 (Core MVP), the backend runs without executing database connection checks.
* **Local Option:** SQLite can optionally be substituted locally using the same SQLAlchemy models if PostgreSQL credentials are not yet configured.
* **Production Database:** Neon connection string supplied via `DATABASE_URL` in `.env`.
