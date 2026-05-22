import json
import os
from typing import Dict, Optional

from src.prompts import SYSTEM_PROMPT, build_dsat_prompt
from src.rules import rule_based_classify

def safe_json_loads(text: str) -> Optional[Dict]:
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                return None
        return None

def analyze_with_openai(case_text: str, api_key: str, model: str = "gpt-4o-mini") -> Dict:
    """Optional OpenAI path. App still works without it via rule-based demo mode."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is not installed. Add openai to requirements.txt.") from exc

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_dsat_prompt(case_text)}
        ],
    )
    raw = response.choices[0].message.content
    parsed = safe_json_loads(raw)
    if not parsed:
        raise ValueError(f"LLM did not return valid JSON: {raw[:500]}")
    return parsed

def analyze_case(case_text: str, provider: str = "Rule-based demo", api_key: str = "", model: str = "gpt-4o-mini") -> Dict:
    if provider == "OpenAI" and api_key:
        try:
            return analyze_with_openai(case_text=case_text, api_key=api_key, model=model)
        except Exception as e:
            fallback = rule_based_classify(case_text)
            fallback["llm_error"] = str(e)
            fallback["fallback_used"] = True
            return fallback
    result = rule_based_classify(case_text)
    result["fallback_used"] = True
    return result
