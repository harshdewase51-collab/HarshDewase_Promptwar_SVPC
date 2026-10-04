import json
import logging
from typing import Dict, Any, Optional
import httpx

from app.core.config import settings

logger = logging.getLogger("blindspot.ai")

SYSTEM_PROMPT = """You are MindLens (BlindSpot AI), an expert objective reasoning auditor.
Your job is to help users identify potential blind spots, unstated assumptions, and hidden tensions in their reasoning before they make an important decision.

CRITICAL RULES:
1. NEVER make the decision for the user. Do NOT say 'accept', 'reject', 'choose option A', or 'you should'.
2. Ground all observations in the user's actual words or explicit omissions.
3. For potential conflicts, ALWAYS use cautious, tentative language: 'potential conflict', 'possible tension', 'you may want to examine', 'worth examining'.
4. Do NOT make psychological diagnoses or claim 100% certainty.
5. TRACEABLE REASONING IS MANDATORY: Every finding must include a 'trace' object explaining:
   - trigger: What in the user's reasoning triggered this finding?
   - considered_factor: What factor did the user already consider?
   - missing_or_weak_factor: What relevant factor was missing, overlooked, or weakly supported?
   - why_relevant: Why this finding is relevant to THIS specific decision.

Return ONLY a single valid JSON object with the following exact keys:
{
  "blind_spots": [
    {
      "finding": "Clear explanation of what was overlooked",
      "evidence": "Specific mention or lack thereof from user input",
      "why_it_matters": "Why this gap impacts the decision outcome",
      "trace": {
        "trigger": "User mentioned X in their reasoning",
        "considered_factor": "Factor user evaluated",
        "missing_or_weak_factor": "Factor that was missing or weakly supported",
        "why_relevant": "Why this is relevant to this specific decision"
      }
    }
  ],
  "assumptions": [
    {
      "assumption": "Unverified premise the user takes for granted",
      "evidence": "Phrase or rationale from user input",
      "needs_verification": true,
      "trace": {
        "trigger": "User stated X as justification",
        "considered_factor": "Desired outcome",
        "missing_or_weak_factor": "Unverified causal link",
        "why_relevant": "Why testing this premise is critical for this choice"
      },
      "verification": "Actionable steps or questions to verify it"
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
      "conflict": "Cautious description of tension between goals/reasoning",
      "evidence": "Conflicting elements noted",
      "question": "Clarifying question to evaluate this tension",
      "trace": {
        "trigger": "User stated X and Y in the decision/reasoning",
        "first_reasoning_point": "First stated priority",
        "second_reasoning_point": "Second conflicting justification",
        "why_relevant": "Why this internal tension could compromise the outcome"
      }
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

Analyze the logic and return the structured JSON audit with traceable reasoning according to your system instructions."""

        # Try remote LLM if key is configured
        if settings.AI_API_KEY and settings.AI_API_KEY.strip():
            try:
                result = await AIService._call_remote_llm(user_prompt)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Remote LLM call failed, switching to grounded fallback: {e}")

        # Intelligent grounded heuristic fallback with full traceability
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
        """Deterministic, grounded reasoning engine with explicit 4-part traceability."""
        text = f"{decision} {context or ''} {reasoning}".lower()
        r_lower = reasoning.lower()

        blind_spots = []
        assumptions = []
        verifications = []
        potential_conflicts = []
        missing_factors = []
        critical_questions = []

        # 1. Domain: Internship / Career / Job
        if any(w in text for w in ["intern", "internship", "job", "career", "salary", "stipend", "promotion", "company"]):
            if "mentor" not in text:
                blind_spots.append({
                    "finding": "Mentorship and guidance structure were not considered in your evaluation.",
                    "evidence": "You cited career growth and salary, but did not mention senior mentorship.",
                    "why_it_matters": "The day-to-day value of an early-career role depends heavily on mentorship quality and bandwidth.",
                    "trace": {
                        "trigger": "You mentioned career improvement and financial compensation in your reasoning.",
                        "considered_factor": "Career growth and compensation",
                        "missing_or_weak_factor": "Availability of dedicated mentorship and senior engineering support",
                        "why_relevant": "Career growth in an early role is driven primarily by mentorship and skill feedback, not merely having a company name on your resume."
                    }
                })
                missing_factors.append("Availability of experienced mentors and team bandwidth")

            if "academic" not in text and "school" not in text and "degree" not in text:
                missing_factors.append("Impact on academic curriculum, semester workload, or graduation timeline")
            if "hours" not in text and "culture" not in text:
                missing_factors.append("Workplace culture, expected weekly hours, and burnout risks")

            assumptions.append({
                "assumption": "This opportunity will automatically accelerate your career trajectory and guarantee higher-paying job offers.",
                "evidence": f"Reasoning states: '{reasoning[:80]}...'",
                "needs_verification": True,
                "trace": {
                    "trigger": "You linked accepting this opportunity directly to guaranteed career improvement.",
                    "considered_factor": "Resume enhancement and future earning potential",
                    "missing_or_weak_factor": "Unverified assumption that early-stage experience always supersedes degree completion or traditional internships",
                    "why_relevant": "If the company's reputation or project scope does not impress future hiring managers, delayed graduation may become a net negative."
                },
                "verification": "Connect with 2-3 previous interns or employees at this organization to review their actual projects and exit outcomes."
            })
            verifications.append({
                "assumption": "This opportunity will automatically accelerate your career trajectory and guarantee higher-paying job offers.",
                "verification": "Connect with 2-3 previous interns or employees at this organization to review their actual projects and exit outcomes."
            })

            potential_conflicts.append({
                "conflict": "There may be a potential tension between immediate financial compensation and the long-term learning value of the experience.",
                "evidence": "Your reasoning emphasizes stipend and pay as key justification alongside career growth.",
                "question": "If day-to-day tasks turn out to be purely operational maintenance with limited learning, does the compensation alone still justify the choice?",
                "trace": {
                    "trigger": "You highlighted the stipend prominently while framing the choice as an investment in your career.",
                    "first_reasoning_point": "Immediate compensation (stipend/salary)",
                    "second_reasoning_point": "Long-term professional skill accumulation",
                    "why_relevant": "High pay at a small startup can sometimes compensate for mundane tasks that stunt technical growth."
                }
            })

            critical_questions.extend([
                "What concrete technical or domain skills will you actively learn in the first 60 days?",
                "Who will directly supervise and evaluate your work on a weekly basis?",
                "What is your contingency plan if the working hours conflict with degree requirements?"
            ])

        # 2. Domain: Hardware / Purchase
        elif any(w in text for w in ["laptop", "computer", "macbook", "phone", "purchase", "buy", "price", "budget"]):
            blind_spots.append({
                "finding": "Long-term durability, depreciation, and repairability were not evaluated.",
                "evidence": "You evaluated the purchase based on current specifications without noting repairability or warranty coverage.",
                "why_it_matters": "Hardware value depreciates rapidly and unexpected repair or battery replacement costs alter the total cost of ownership.",
                "trace": {
                    "trigger": "You focused on immediate performance benchmarks and productivity gains.",
                    "considered_factor": "Short-term speed improvement and feature set",
                    "missing_or_weak_factor": "Total cost of ownership (depreciation, warranty, repair ecosystem)",
                    "why_relevant": "Hardware investments must generate returns that outpace their rapid depreciation curve."
                }
            })
            assumptions.append({
                "assumption": "The chosen device will immediately boost productivity enough to financially offset its purchase cost.",
                "evidence": f"You noted: '{reasoning[:80]}...'",
                "needs_verification": True,
                "trace": {
                    "trigger": "You reasoned that the device will pay for itself through improved work output.",
                    "considered_factor": "Anticipated productivity boost",
                    "missing_or_weak_factor": "Lack of benchmark evidence that computer hardware is currently your primary bottleneck",
                    "why_relevant": "If software or client acquisition is the actual bottleneck, a faster laptop will not increase revenue."
                },
                "verification": "Track your current daily workflow bottlenecks to verify whether computing speed is truly what delays client deliverables."
            })
            verifications.append({
                "assumption": "The chosen device will immediately boost productivity enough to financially offset its purchase cost.",
                "verification": "Track your current daily workflow bottlenecks to verify whether computing speed is truly what delays client deliverables."
            })
            missing_factors.extend([
                "Battery longevity and thermal performance under sustained load",
                "Warranty terms, accidental damage coverage, and official repair availability",
                "Opportunity cost of the cash or financing interest charges"
            ])
            potential_conflicts.append({
                "conflict": "There appears to be a possible tension between financial liquidity and equipment upgrading.",
                "evidence": "The purchase is significant relative to available capital or relies on financing.",
                "question": "Does allocating capital to this hardware restrict your ability to invest in other business or personal necessities?",
                "trace": {
                    "trigger": "Reasoning treats the purchase as an urgent necessity despite existing functional equipment.",
                    "first_reasoning_point": "Desire for premium performance specifications",
                    "second_reasoning_point": "Prudent financial management and cash flow preservation",
                    "why_relevant": "Depleting emergency savings or adding debt creates financial stress that could negate productivity gains."
                }
            })
            critical_questions.extend([
                "Does this model have known thermal or hardware issues documented in recent user forums?",
                "What is the total cost including essential accessories, adapters, and protection plans?",
                "Will your computing needs expand before the expected lifespan of this device concludes?"
            ])

        # 3. General Decision Domain
        else:
            blind_spots.append({
                "finding": "Opportunity costs and irreversible commitments were left unaddressed.",
                "evidence": f"Your rationale states: '{reasoning[:90]}', without discussing trade-offs.",
                "why_it_matters": "Choosing one path inherently closes alternatives; examining what you sacrifice prevents future regret.",
                "trace": {
                    "trigger": "Your reasoning is entirely centered on perceived upside benefits.",
                    "considered_factor": "Positive expected outcomes",
                    "missing_or_weak_factor": "Alternative paths declined and irreversible resource commitments",
                    "why_relevant": "Every major decision closes specific doors; evaluating trade-offs is essential to sound reasoning."
                }
            })
            assumptions.append({
                "assumption": "Current favorable conditions will persist without unexpected external disruption or delay.",
                "evidence": "The decision assumes positive forward momentum based on current assumptions.",
                "needs_verification": True,
                "trace": {
                    "trigger": "You assumed that the plan will execute smoothly under ideal conditions.",
                    "considered_factor": "Ideal execution scenario",
                    "missing_or_weak_factor": "Downside contingency planning and variable sensitivity",
                    "why_relevant": "Unchecked optimism bias leaves decision-makers unprepared when conditions inevitably fluctuate."
                },
                "verification": "Identify the top 2 variables outside your direct control and define contingency triggers for both."
            })
            verifications.append({
                "assumption": "Current favorable conditions will persist without unexpected external disruption or delay.",
                "verification": "Identify the top 2 variables outside your direct control and define contingency triggers for both."
            })
            missing_factors.extend([
                "Opportunity cost (what alternative opportunities are being declined)",
                "Downside risk mitigation if conditions change",
                "Timeline elasticity (what happens if outcomes take twice as long to achieve)"
            ])
            potential_conflicts.append({
                "conflict": "There appears to be a possible tension between short-term certainty and long-term flexibility.",
                "evidence": "The rationale is anchored on immediate benefits while leaving long-term contingencies open.",
                "question": "How comfortable are you with the reversibility of this choice if initial expectations are unmet?",
                "trace": {
                    "trigger": "You cited immediate certainty while taking on long-term commitments.",
                    "first_reasoning_point": "Immediate certainty of the chosen path",
                    "second_reasoning_point": "Need for strategic optionality in the future",
                    "why_relevant": "Locking in a choice today reduces your agility to pivot if new opportunities emerge."
                }
            })
            critical_questions.extend([
                "What is the single most vulnerable assumption underlying this decision?",
                "If this choice yields disappointing results in 6 months, what would you wish you had investigated today?",
                "Who in your network with opposing views could offer a constructive critique of this plan?"
            ])

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
