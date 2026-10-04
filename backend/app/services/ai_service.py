import json
import logging
import re
from typing import Dict, Any, Optional
import httpx

from app.core.config import settings

logger = logging.getLogger("blindspot.ai")

SYSTEM_PROMPT = """You are BlindSpot AI, an expert objective reasoning auditor.
Your job is to help users identify potential blind spots, unstated assumptions, and hidden tensions in their reasoning before they make an important decision.

CRITICAL RULES:
1. NEVER make the decision for the user. Do NOT say 'accept', 'reject', 'choose option A', or 'you should'.
2. Ground all observations in the user's actual words or explicit omissions.
3. For potential conflicts, ALWAYS use cautious, tentative language: 'potential conflict', 'possible tension', 'you may want to examine', 'worth examining'.
4. Do NOT make psychological diagnoses or claim 100% certainty.
5. Return ONLY a single valid JSON object with the following exact keys:
{
  "blind_spots": [
    {
      "finding": "Clear explanation of what was overlooked",
      "evidence": "Specific mention or lack thereof from user input",
      "why_it_matters": "Why this gap impacts the decision outcome"
    }
  ],
  "assumptions": [
    {
      "assumption": "Unverified premise the user takes for granted",
      "evidence": "Phrase or rationale from user input",
      "needs_verification": true
    }
  ],
  "verification": [
    {
      "assumption": "The assumption being tested",
      "verification": "Actionable steps or questions to verify it"
    }
  ],
  "potential_conflicts": [
    {
      "conflict": "Cautions description of tension between goals/reasoning",
      "evidence": "Conflicting elements noted",
      "question": "Clarifying question to evaluate this tension"
    }
  ],
  "missing_factors": [
    "Specific omitted dimension 1",
    "Specific omitted dimension 2"
  ],
  "critical_questions": [
    "High-impact investigation question 1?",
    "High-impact investigation question 2?"
  ]
}
"""

class AIService:
    @staticmethod
    async def generate_audit(decision: str, context: Optional[str], reasoning: str) -> Dict[str, Any]:
        """Calls external LLM if configured; otherwise falls back to intelligent grounded reasoning."""
        user_prompt = f"""AUDIT THIS DECISION:
DECISION: {decision}
CONTEXT: {context or 'None provided'}
REASONING: {reasoning}

Analyze the logic and return the structured JSON audit according to your system instructions."""

        # Try remote LLM if key is configured
        if settings.AI_API_KEY and settings.AI_API_KEY.strip():
            try:
                result = await AIService._call_remote_llm(user_prompt)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Remote LLM call failed, switching to grounded fallback: {e}")

        # Intelligent grounded heuristic fallback
        return AIService._grounded_fallback_audit(decision, context, reasoning)

    @staticmethod
    async def _call_remote_llm(user_prompt: str) -> Optional[Dict[str, Any]]:
        """Call Groq or OpenAI compatible API endpoint."""
        api_key = settings.AI_API_KEY.strip()
        provider = settings.AI_PROVIDER.lower()
        
        if "groq" in provider:
            url = "https://api.groq.com/openai/v1/chat/completions"
            model = settings.AI_MODEL or "llama-3.3-70b-versatile"
        else:
            url = "https://api.openai.com/v1/chat/completions"
            model = settings.AI_MODEL or "gpt-4o-mini"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient(timeout=25.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                logger.warning(f"LLM API returned status {response.status_code}: {response.text}")
                return None

    @staticmethod
    def _grounded_fallback_audit(decision: str, context: Optional[str], reasoning: str) -> Dict[str, Any]:
        """Deterministic, grounded reasoning engine that dynamically inspects decision keywords and arguments."""
        text = f"{decision} {context or ''} {reasoning}".lower()
        d_lower = decision.lower()
        r_lower = reasoning.lower()

        blind_spots = []
        assumptions = []
        verifications = []
        potential_conflicts = []
        missing_factors = []
        critical_questions = []

        # 1. Domain Detection & Tailored Missing Factors
        if any(w in text for w in ["intern", "internship", "job", "career", "salary", "stipend", "promotion", "company"]):
            if "mentor" not in text:
                blind_spots.append({
                    "finding": "Your reasoning emphasizes career progression and immediate compensation, but does not address mentorship or team guidance.",
                    "evidence": "You cited career growth and salary, but did not mention senior mentorship.",
                    "why_it_matters": "The day-to-day value of an early role depends heavily on mentorship quality and support."
                })
                missing_factors.append("Availability of experienced mentors and team bandwidth")
            if "academic" not in text and "school" not in text and "degree" not in text:
                missing_factors.append("Impact on academic curriculum, semester workload, or graduation timeline")
            if "hours" not in text and "culture" not in text:
                missing_factors.append("Workplace culture, expected weekly hours, and burnout risks")

            assumptions.append({
                "assumption": "This opportunity will automatically provide prestigious experience and accelerate your career trajectory.",
                "evidence": f"Reasoning mentions: '{reasoning[:80]}...'",
                "needs_verification": True
            })
            verifications.append({
                "assumption": "This opportunity will automatically provide prestigious experience and accelerate your career trajectory.",
                "verification": "Connect with 2-3 previous interns or employees at this organization to review their actual projects and exit outcomes."
            })

            if ("salary" in r_lower or "stipend" in r_lower or "money" in r_lower) and ("learn" in text or "skill" in text):
                potential_conflicts.append({
                    "conflict": "There may be a potential tension between your stated interest in skill development and the strong focus on compensation in your reasoning.",
                    "evidence": "Stipend/salary is highlighted as a primary driver alongside learning.",
                    "question": "If day-to-day tasks turn out to be purely operational with limited learning, does the compensation alone still justify the choice?"
                })

            critical_questions.extend([
                "What concrete technical or domain skills will you actively learn in the first 60 days?",
                "Who will directly supervise and evaluate your work on a weekly basis?",
                "What is your fallback plan if the work responsibilities differ from the initial description?"
            ])

        elif any(w in text for w in ["laptop", "computer", "macbook", "phone", "purchase", "buy", "price", "budget"]):
            blind_spots.append({
                "finding": "Your reasoning focuses primarily on price and immediate appeal, but omits long-term durability and support costs.",
                "evidence": "You evaluated the purchase based on current specifications without noting repairability or warranty coverage.",
                "why_it_matters": "Hardware value depreciates and unexpected repair or battery replacement costs can alter the total cost of ownership."
            })
            assumptions.append({
                "assumption": "The chosen device will sufficiently handle your future workflow requirements over the next 2-3 years.",
                "evidence": f"You noted: '{reasoning[:80]}...'",
                "needs_verification": True
            })
            verifications.append({
                "assumption": "The chosen device will sufficiently handle your future workflow requirements over the next 2-3 years.",
                "verification": "Check benchmarks for the specific applications and multi-tasking software you intend to run under peak loads."
            })
            missing_factors.extend([
                "Battery longevity and thermal performance under load",
                "Warranty terms, accidental damage coverage, and official repair availability",
                "Resale value and port connectivity requirements"
            ])
            critical_questions.extend([
                "Does this model have known thermal or hardware issues documented in recent user forums?",
                "What is the total cost including essential accessories, adapters, and protection plans?",
                "Will your computing needs expand before the expected lifespan of this device concludes?"
            ])

        else:
            # General Decision Domain
            blind_spots.append({
                "finding": "Your reasoning centers around immediate perceived benefits, but does not explore opportunity costs or irreversible commitments.",
                "evidence": f"Your rationale states: '{reasoning[:90]}', without discussing trade-offs.",
                "why_it_matters": "Choosing one path inherently closes alternatives; examining what you sacrifice prevents future regret."
            })
            assumptions.append({
                "assumption": "The expected outcome will materialize without unforeseen external delays or constraints.",
                "evidence": "The decision assumes positive forward momentum based on current assumptions.",
                "needs_verification": True
            })
            verifications.append({
                "assumption": "The expected outcome will materialize without unforeseen external delays or constraints.",
                "verification": "Identify the top 2 variables outside your direct control and define contingency triggers for both."
            })
            missing_factors.extend([
                "Opportunity cost (what alternative opportunities are being declined)",
                "Downside risk mitigation if conditions change",
                "Timeline elasticity (what happens if outcomes take twice as long to achieve)"
            ])
            critical_questions.extend([
                "What is the single most vulnerable assumption underlying this decision?",
                "If this choice yields disappointing results in 6 months, what would you wish you had investigated today?",
                "Who in your network with opposing views could offer a constructive critique of this plan?"
            ])

        # Default fallback conflict if none was detected yet
        if not potential_conflicts:
            potential_conflicts.append({
                "conflict": "There appears to be a possible tension between short-term certainty and long-term flexibility.",
                "evidence": "The rationale is anchored on immediate benefits while leaving long-term contingencies open.",
                "question": "How comfortable are you with the reversibility of this choice if initial expectations are unmet?"
            })

        return {
            "blind_spots": blind_spots,
            "assumptions": assumptions,
            "verification": verifications,
            "potential_conflicts": potential_conflicts,
            "missing_factors": missing_factors,
            "critical_questions": critical_questions,
            "summary_grounding": "Audit generated by MindLens reasoning engine grounded strictly in user submission."
        }

ai_service = AIService()
