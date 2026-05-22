import pandas as pd
from typing import List
from src.llm_client import analyze_case
from src.preprocessing import prepare_cases

OUTPUT_COLUMNS = [
    "dsat_type",
    "root_cause_category",
    "root_cause_summary",
    "agent_accountability",
    "evidence_from_case",
    "coaching_recommendation",
    "customer_recovery_action",
    "severity",
    "confidence_score",
]

def analyze_dataframe(
    df: pd.DataFrame,
    text_columns: List[str],
    provider: str = "Rule-based demo",
    api_key: str = "",
    model: str = "gpt-4o-mini",
    max_rows: int = 50,
) -> pd.DataFrame:
    work = prepare_cases(df, text_columns)
    work = work.head(max_rows).copy()

    results = []
    for _, row in work.iterrows():
        result = analyze_case(
            row["case_text_for_analysis"],
            provider=provider,
            api_key=api_key,
            model=model,
        )
        results.append(result)

    result_df = pd.DataFrame(results)
    for col in OUTPUT_COLUMNS:
        if col not in result_df.columns:
            result_df[col] = None

    combined = pd.concat([work.reset_index(drop=True), result_df.reset_index(drop=True)], axis=1)
    return combined

def build_executive_summary(result_df: pd.DataFrame) -> str:
    total = len(result_df)
    if total == 0:
        return "No DSAT cases analyzed."

    type_counts = result_df["dsat_type"].value_counts(dropna=False)
    root_counts = result_df["root_cause_category"].value_counts(dropna=False).head(5)
    high_sev = int((result_df["severity"] == "High").sum()) if "severity" in result_df else 0

    lines = [
        f"{total} DSAT cases were analyzed.",
        "DSAT type distribution: " + ", ".join([f"{idx}: {cnt}" for idx, cnt in type_counts.items()]),
        "Top root causes: " + ", ".join([f"{idx}: {cnt}" for idx, cnt in root_counts.items()]),
        f"High severity cases identified: {high_sev}.",
        "Recommended focus areas: review repeated agent-driven categories, validate mixed-accountability cases with QA, and escalate repeated non-agent-driven process issues to operations."
    ]
    return "\n".join(lines)
