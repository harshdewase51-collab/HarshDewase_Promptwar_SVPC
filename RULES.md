# Development & Product Rules

## Project Name: MindLens

---

> [!IMPORTANT]
> These rules are non-negotiable guidelines for building, maintaining, and presenting MindLens. Every team member and automated assistant must strictly abide by them.

---

## A. Product Rules
1. **Never Make the Decision:** MindLens will NEVER advise, instruct, or declare which option the user should choose. (No: *"You should accept the internship."* Yes: *"Here are the unaddressed factors in your reasoning."*)
2. **Audit the Reasoning, Not the Person:** Focus strictly on the logic, assumptions, evidence, and missing context provided in the text.
3. **Strict Grounding in User Input:** Every single identified blind spot or tension must directly reference specific points the user wrote, or directly point out an obvious situational factor missing from their context.
4. **No Fabricated Evidence:** Never invent imaginary company reviews, fake statistics, or external facts the user did not supply.
5. **No Unsupported Claims:** Do not claim certainty where none exists. Always frame observations around what the user *has* or *has not* considered.

---

## B. AI Rules
1. **Structured JSON Output Only:** The AI Reasoning Engine must exclusively return a valid, parseable JSON payload adhering to the predefined schema. No conversational filler, preambles, or unformatted markdown.
2. **Fixed Analysis Categories:** The engine must always produce the 6 core categories:
   * Evidence-Linked Blind Spots
   * Hidden Assumptions
   * Assumption Verification Actions
   * Potential Conflicts / Tensions
   * Context-Specific Missing Factors
   * Critical Questions to Consider
3. **Cautious and Respectful Language:** Always use measured, tentative phrasing for conflicts:
   * *"A potential conflict you may want to examine..."*
   * *"There appears to be a possible tension between..."*
   * *"You may want to consider..."*
4. **Zero Psychological Diagnoses:** Never use clinical or psychological labels (e.g., do not say *"You are suffering from cognitive dissonance"* or *"This shows narcissism/delusion"*). Speak purely in terms of argumentation and decision variables.
5. **Calibrated Confidence:** Never label an assumption as a guaranteed fact or certainty. Remind the user that the audit highlights points for exploration, not definitive verdicts.

---

## C. Development Rules
1. **Resist Over-Engineering:** Keep the solution direct, minimal, and demonstrably working. Do not add complex state machines, micro-services, or redundant abstractions.
2. **Zero Bloat Dependencies:** Do not add third-party libraries for trivial tasks that can be done with standard vanilla JavaScript or Python libraries.
3. **Preserve Architecture Stability:** Do not alter the directory structure or switch frameworks mid-hackathon without explicit consensus.
4. **Code Reuse:** Reuse utility functions, styling tokens, and modular components rather than duplicating logic.
5. **Readable, Documented Functions:** Keep functions small (under 40 lines where feasible), single-responsibility, and accompanied by brief explanatory docstrings.

---

## D. Security Rules
1. **Zero Client-Side Secret Exposure:** Never put `LLM_API_KEY`, JWT secrets, or database credentials in frontend code or client-accessible files.
2. **Strict `.env` Management:** All sensitive variables must be loaded via backend environment variables.
3. **Never Commit Secrets:** `.env` and sensitive credentials must be included in `.gitignore` at all times.
4. **Always Validate on the Backend:** Never rely solely on frontend client-side validation. Enforce constraints using Pydantic schemas in FastAPI.
5. **Secure Password Hashing:** Always hash passwords with `bcrypt` (minimum 12 rounds) before persistence.
6. **SQL Injection Defense:** Use parameterized queries via SQLAlchemy ORM; never concatenate user input into raw SQL queries.
7. **Protected Endpoints:** Secure authenticated routes using FastAPI dependencies (`Depends(get_current_user)`).

---

## E. Hackathon Rules
1. **The 3-Hour Constraint:** Time is the scarcest resource. Every task must be evaluated against its delivery deadline.
2. **Core Flow First:** The end-to-end user loop (Input → AI Audit → Display Results) has the absolute highest priority.
3. **Deployment is Mandatory:** A working demo accessible via a public URL is infinitely more valuable than an unfinished feature running only on `localhost`.
4. **Working Demo > Feature Count:** A rock-solid, bug-free core audit with 0 errors beats a half-baked dashboard with broken authentication.
5. **Decoupled Architecture:** Ensure the core AI auditing feature works even if the database is unconfigured or unreachable.

---

## F. Documentation Rules
1. **Explicit Implementation Status:**
   * If a feature or component is not yet coded and running, explicitly label it:  
     `NOT IMPLEMENTED`
   * If a feature is planned or recommended for later phases, label it:  
     `RECOMMENDED, NOT IMPLEMENTED` or `PLANNED / NOT IMPLEMENTED YET`
2. **Zero Deceptive Claims:** Never state in documentation, README, or presentations that a feature is functional unless it has been built and verified.
3. **Single Source of Truth:** Keep all 7 documentation files harmonized. If a change is made to an endpoint or schema, update the corresponding documentation files immediately.
