import json

SYSTEM_PROMPT = """
You are a senior customer experience QA analyst for a contact center.

Your task is to analyze a customer dissatisfaction case and classify the DSAT root cause.

Definitions:
- Agent-Driven DSAT: dissatisfaction was mainly caused by agent behavior such as incorrect information, lack of empathy, poor ownership, weak probing, delayed response, poor tone, or failure to follow up.
- Non-Agent-Driven DSAT: dissatisfaction was mainly caused by factors outside agent control such as product issue, system issue, policy limitation, delivery delay, repair delay, stock unavailability, pricing/tariff concern, or business process limitation.
- Mixed Accountability: both agent handling and process/business factors contributed.
- Needs QA Validation: information is insufficient or confidence is low.

Return only valid JSON. Do not include markdown.
"""

def build_dsat_prompt(case_text: str) -> str:
    schema = {
        "dsat_type": "Agent-Driven DSAT | Non-Agent-Driven DSAT | Mixed Accountability | Needs QA Validation",
        "root_cause_category": "specific root cause",
        "root_cause_summary": "1-3 sentence explanation",
        "agent_accountability": "High | Medium | Low | Unknown",
        "evidence_from_case": "specific evidence from the case",
        "coaching_recommendation": "specific coaching action",
        "customer_recovery_action": "specific action to recover the customer experience",
        "severity": "High | Medium | Low",
        "confidence_score": "number between 0 and 1"
    }
    return f"""
Analyze this DSAT case and return the result using this JSON schema:
{json.dumps(schema, indent=2)}

Case details:
{case_text}
""".strip()
