from dataclasses import dataclass
from typing import List

DSAT_TYPES = [
    "Agent-Driven DSAT",
    "Non-Agent-Driven DSAT",
    "Mixed Accountability",
    "Needs QA Validation",
]

AGENT_DRIVEN_CATEGORIES = [
    "Incorrect Information",
    "Lack of Empathy",
    "Poor Ownership",
    "Delayed Response",
    "Incomplete Resolution",
    "Weak Probing",
    "Poor Explanation",
    "Unnecessary Transfer",
    "Failure to Follow Up",
    "Unprofessional Tone",
    "Policy Miscommunication",
    "Escalation Mishandling",
]

NON_AGENT_DRIVEN_CATEGORIES = [
    "Product Issue",
    "System Issue",
    "Policy Limitation",
    "Delivery Delay",
    "Repair Delay",
    "Stock Unavailability",
    "Pricing or Tariff Concern",
    "Previous Case Issue",
    "Customer Expectation Mismatch",
    "Third-Party Dependency",
    "Business Process Limitation",
]

NEEDS_REVIEW_CATEGORIES = [
    "Insufficient Information",
    "Mixed Accountability",
    "Needs QA Validation",
]

@dataclass
class AnalyzerConfig:
    confidence_review_threshold: float = 0.70
    max_text_chars: int = 8000
    default_text_columns: List[str] = None
