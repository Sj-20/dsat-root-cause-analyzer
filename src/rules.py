from typing import Dict, List, Tuple

AGENT_KEYWORDS = {
    "Lack of Empathy": ["no empathy", "ignored", "generic", "scripted", "did not acknowledge", "not helpful", "rude", "dismissive"],
    "Incorrect Information": ["wrong information", "incorrect", "misinformed", "not accurate", "false promise", "free replacement"],
    "Poor Ownership": ["no ownership", "transferred", "repeat myself", "did not explain", "unclear next step"],
    "Weak Probing": ["did not ask", "no serial", "no order number", "weak probing", "did not verify"],
    "Failure to Follow Up": ["no follow-up", "promised callback", "never called", "not updated"],
    "Unprofessional Tone": ["rude", "dismissive", "ended chat", "unprofessional", "bad attitude"],
}

NON_AGENT_KEYWORDS = {
    "Policy Limitation": ["policy", "warranty expired", "not covered", "outside warranty", "paid repair"],
    "Repair Delay": ["repair delay", "repair center", "backlog", "waiting time"],
    "Product Issue": ["product failed", "defect", "malfunction", "technical issue"],
    "Stock Unavailability": ["out of stock", "no stock", "not available"],
    "Pricing or Tariff Concern": ["tariff", "import fee", "price", "charge", "too high"],
    "System Issue": ["system issue", "outage", "system did not", "technical error"],
    "Previous Case Issue": ["previous case", "third contact", "previous promised", "already contacted"],
}

def score_keywords(text: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    text_l = text.lower()
    agent_scores = {
        category: sum(1 for kw in keywords if kw in text_l)
        for category, keywords in AGENT_KEYWORDS.items()
    }
    non_agent_scores = {
        category: sum(1 for kw in keywords if kw in text_l)
        for category, keywords in NON_AGENT_KEYWORDS.items()
    }
    return agent_scores, non_agent_scores

def rule_based_classify(text: str) -> Dict:
    """Simple deterministic fallback classifier. Useful for demo mode without paid LLM APIs."""
    agent_scores, non_agent_scores = score_keywords(text)
    total_agent = sum(agent_scores.values())
    total_non_agent = sum(non_agent_scores.values())

    if len(text.strip()) < 80:
        return {
            "dsat_type": "Needs QA Validation",
            "root_cause_category": "Insufficient Information",
            "root_cause_summary": "The available case details are too limited to determine the main driver of dissatisfaction.",
            "agent_accountability": "Unknown",
            "evidence_from_case": "The case text does not contain enough details for a reliable classification.",
            "coaching_recommendation": "Ask QA/TL to review the full interaction transcript before assigning accountability.",
            "customer_recovery_action": "Contact the customer to clarify the unresolved concern and provide a clear next step.",
            "severity": "Medium",
            "confidence_score": 0.55,
        }

    if total_agent > 0 and total_non_agent > 0:
        dsat_type = "Mixed Accountability"
        category = max({**agent_scores, **non_agent_scores}, key={**agent_scores, **non_agent_scores}.get)
        accountability = "Medium"
        confidence = min(0.82, 0.62 + 0.05 * (total_agent + total_non_agent))
    elif total_agent > total_non_agent:
        dsat_type = "Agent-Driven DSAT"
        category = max(agent_scores, key=agent_scores.get)
        accountability = "High"
        confidence = min(0.90, 0.65 + 0.06 * total_agent)
    elif total_non_agent > total_agent:
        dsat_type = "Non-Agent-Driven DSAT"
        category = max(non_agent_scores, key=non_agent_scores.get)
        accountability = "Low"
        confidence = min(0.90, 0.65 + 0.06 * total_non_agent)
    else:
        dsat_type = "Needs QA Validation"
        category = "Insufficient Information"
        accountability = "Unknown"
        confidence = 0.58

    severity = "High" if any(x in text.lower() for x in ["rude", "wrong information", "third contact", "no follow-up"]) else "Medium"

    if dsat_type == "Agent-Driven DSAT":
        coaching = f"Coach the agent on {category.lower()}, empathy, ownership, and clear next-step setting."
        recovery = "Follow up with the customer, acknowledge the inconvenience, and provide a specific resolution timeline."
    elif dsat_type == "Non-Agent-Driven DSAT":
        coaching = "No major handling issue detected. Reinforce positive positioning, empathy, and alternative solution offering."
        recovery = "Provide a transparent update and set expectations based on policy/process limitations."
    elif dsat_type == "Mixed Accountability":
        coaching = f"Review both the process gap and the agent opportunity related to {category.lower()}."
        recovery = "Escalate the process issue and send a clear recovery update to the customer."
    else:
        coaching = "Send the case for manual QA validation due to limited information."
        recovery = "Request more case details before deciding next action."

    return {
        "dsat_type": dsat_type,
        "root_cause_category": category,
        "root_cause_summary": f"The case appears to be classified as {dsat_type} with the main driver related to {category}.",
        "agent_accountability": accountability,
        "evidence_from_case": text[:450],
        "coaching_recommendation": coaching,
        "customer_recovery_action": recovery,
        "severity": severity,
        "confidence_score": round(confidence, 2),
    }
