# Product Requirements Document (PRD)

## Project Name: MindLens

---

## 1. Problem Statement
When individuals make high-stakes personal, academic, or professional decisions, they rarely suffer from a lack of intelligence or goodwill. Instead, they fall prey to predictable cognitive vulnerabilities: confirmation bias, optimistic overconfidence, unexamined assumptions, and situational tunnel vision. Most current conversational AI tools act as "sycophantic advisors" or "decision generators"—they either validate the user's existing bias or arrogantly decree what decision the user *should* make. This creates dangerous liability, hallucinated certainty, and robs the user of genuine agency.

---

## 2. Problem in Simple Words
People convince themselves their choices make total sense because they only focus on the factors that support what they want to believe. They don't need an AI to dictate what to do. They need an objective, calm mirror that points out what they forgot to consider before they pull the trigger.

---

## 3. Target Users
* **Students & Recent Graduates:** Evaluating internships, job offers, majors, or graduate programs with limited life experience.
* **Early-Career Professionals:** Navigating role transitions, salary negotiations, company switches, or startup pivots.
* **Indie Builders & Founders:** Weighing feature releases, pricing models, partnerships, or resource allocations under time pressure.
* **Everyday Decision-Makers:** Anyone contemplating significant lifestyle, financial, or commitments needing a second pair of eyes on their logic.

---

## 4. Core Pain Point
* **The "Reasoning Blind Spot":** Users mistake internal conviction for sound reasoning. They formulate a justification based on 1–2 salient benefits (e.g., "the pay is high") while remaining oblivious to hidden assumptions, conflicting priorities, and unaddressed risks (e.g., burnout, career trajectory, mentor absence).

---

## 5. Product Goal
To deliver an objective, grounded, non-prescriptive reasoning audit for any decision in under 15 seconds, exposing hidden assumptions, potential tensions, and omitted factors without making the decision for the user.

---

## 6. Proposed Solution
MindLens is a focused web application where the user provides three inputs:
1. **Decision:** What specific choice is on the table?
2. **Context:** What is the background situation, timeline, constraints, and stakes?
3. **Reasoning:** Why does the user believe this is the right decision?

The AI Reasoning Engine parses the relationship between the decision, context, and reasoning. It produces a structured audit across six distinct dimensions:
1. Evidence-Linked Blind Spots
2. Hidden Assumptions
3. Assumption Verification Actions
4. Potential Conflicts / Tensions
5. Context-Specific Missing Factors
6. Critical Questions to Consider

---

## 7. Core Value Proposition
> **“We don't make the decision for you. We audit the reasoning behind your decision.”**  
> *MindLens doesn't tell you what decision to make; it tells you what you might be missing before you make it.*

---

## 8. Main User Journey
1. **Landing & Intake:** User lands on a clean, single-purpose interface with clear prompt guidance.
2. **Input Formulation:** User enters their Decision, Context, and Reasoning into guided text areas with example prompts for inspiration.
3. **Audit Execution:** User clicks "Audit My Reasoning". A clear auditing indicator reassures the user that analysis is underway.
4. **Structured Review:** The user is presented with categorized, color-coded audit cards highlighting blind spots, assumptions, verifications, tensions, missing factors, and critical questions.
5. **Reflection & Action:** The user reviews the verification steps and questions, reflects on their true priorities, and makes an informed choice with their eyes open.
6. *(Optional / Should-Have)* **Save & Track:** User signs in to save the decision audit to their personal dashboard history.

---

## 9. Functional Requirements
* **FR-1: Triple Input Interface:** Dedicated input fields for Decision, Context, and Reasoning with character counter and baseline validation (minimum 20 characters for reasoning).
* **FR-2: Reasoning Engine API:** Backend endpoint accepting the three inputs and sending an audit prompt to the LLM.
* **FR-3: Structured Schema Enforcement:** Guaranteed JSON response parsing containing all six audit categories.
* **FR-4: Evidence Grounding:** AI output must explicitly cite user phrases or clear contextual gaps.
* **FR-5: Cautious Language Standard:** Automatic enforcement of non-dogmatic phrasing for conflicts ("potential conflict", "possible tension").
* **FR-6: Result Presentation:** Responsive card-based layout grouping findings logically for quick scanning.
* **FR-7: Session Persistence:** State preserved on client during the active session.

---

## 10. Must-Have Features (Core MVP)
| Feature | Description | Status |
| :--- | :--- | :--- |
| **Decision Input** | Single-line or compact textarea capturing the concrete choice | **Planned** |
| **Context Input** | Textarea capturing background, timeline, financial/personal constraints | **Planned** |
| **Reasoning Input** | Textarea capturing the user's rationale, logic, and current beliefs | **Planned** |
| **AI Reasoning Engine** | FastAPI service interfacing with LLM via strict structured prompts | **Planned** |
| **Evidence-Linked Blind Spots** | 2–3 blind spots explicitly grounded in user statements or key omissions | **Planned** |
| **Hidden Assumptions** | 2–3 unstated premises the user takes for granted | **Planned** |
| **Verification Suggestions** | Practical, concrete questions/actions to validate each assumption | **Planned** |
| **Potential Conflicts** | Identification of internal contradictions or tensions using gentle phrasing | **Planned** |
| **Missing Factors** | Important dimensions (e.g., long-term impact, health, costs) left out | **Planned** |
| **Critical Questions** | 3–4 high-impact self-reflection questions | **Planned** |
| **Result Page View** | Clean, accessible presentation with distinct visual blocks | **Planned** |

---

## 11. Should-Have Features
* **User Authentication:** Email/password registration and login with JWT and bcrypt hashing.
* **Audit Persistence:** Save decisions and resulting audits into a PostgreSQL / Neon database.
* **History Dashboard:** List view of previously audited decisions with timestamp and summary.
* **Copy / Export:** One-click copy of the audit summary to clipboard.

---

## 12. Bonus Features (Only if Time Remains)
* **Reflection Loop:** "Re-audit" button allowing the user to update their reasoning in response to the audit.
* **Export to Markdown / PDF:** Downloadable decision brief.
* **Voice Input:** Web Speech API integration for dictating reasoning.
* **Polished Micro-Animations:** Subtle transitions and card reveals.

---

## 13. Non-Goals
* **No Decision Arbitrating:** MindLens will NEVER say "You should do X" or "Option A is better than Option B".
* **No Psychological Profiling:** No diagnosing cognitive deficits, mental health, or personality traits.
* **No Real-Time Web Scraping / Private Fact Verification:** The AI audits the internal logic presented, rather than researching live employer reviews or financial stock prices.
* **No Complex Multi-Agent Swarms:** Avoid heavy multi-step agent chains that increase latency beyond 15 seconds.

---

## 14. AI Responsibilities
* Parse unstructured user thoughts into clear premise-conclusion relationships.
* Detect logical leaps where conclusions do not follow from context or reasoning.
* Ground every observation in the specific text supplied by the user.
* Format all outputs cleanly into rigid JSON for seamless UI rendering.

---

## 15. AI Limitations
* The model only knows what the user shares.
* Cannot guarantee real-world future outcomes.
* May struggle if user inputs are deliberately nonsensical, sarcastic, or excessively terse (mitigated by front-end minimum length validation).

---

## 16. Trust & Safety Rules
1. **Zero Hallucinated Context:** Never claim the user said something they did not say.
2. **Cautious Conflict Language:** Always prefix contradictions with respectful qualifiers ("You may want to examine a possible tension between...").
3. **No Moralizing:** Maintain an objective, supportive analytical tone.
4. **User Sovereignty:** Prominently display the notice: *"MindLens provides logical auditing for self-reflection. You retain full responsibility for your decisions."*

---

## 17. MVP Scope vs. Future Scope
* **Hackathon MVP Scope:** A responsive React + FastAPI web application accepting Decision, Context, and Reasoning, generating an instant 6-category structured audit via LLM, and rendering it cleanly. Database and Auth are decoupled so core AI value is demonstrable first.
* **Future Scope:** Multi-alternative comparisons (Option A vs. Option B matrix), team decision auditing with multiple stakeholder perspectives, integrations with Notion/Slack, and follow-up outcome tracking (e.g., "Did your decision pan out after 3 months?").

---

## 18. Success Criteria
* **Speed:** Audit generated and rendered within 10–15 seconds.
* **Clarity:** Results instantly understandable to a non-technical evaluator within 30 seconds of reading.
* **Relevance:** The audit feels tailor-made to the specific dilemma (demonstrated using the standard Internship Dilemma test case).
* **Reliability:** 100% valid JSON rendering with zero UI crashes during the demo.

---

## 19. Hackathon Constraints
* **Total Time:** ~3 hours end-to-end.
* **Developer Level:** Beginner/intermediate developer—all code must be clean, modular, and easy to explain during judging.
* **Execution Priority:** Working, demonstrable core loop precedes optional database persistence and authentication.
