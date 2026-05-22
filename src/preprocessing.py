import pandas as pd
from typing import List

def read_input_file(uploaded_file) -> pd.DataFrame:
    """Read CSV or Excel from Streamlit upload."""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    raise ValueError("Unsupported file format. Please upload CSV or Excel.")

def combine_text_columns(df: pd.DataFrame, text_columns: List[str], max_chars: int = 8000) -> pd.Series:
    """Combine selected columns into one case text field."""
    if not text_columns:
        raise ValueError("Please select at least one text column.")

    def row_to_text(row):
        parts = []
        for col in text_columns:
            value = row.get(col, "")
            if pd.notna(value) and str(value).strip():
                parts.append(f"{col}: {str(value).strip()}")
        combined = "\n".join(parts)
        return combined[:max_chars]

    return df.apply(row_to_text, axis=1)

def prepare_cases(df: pd.DataFrame, text_columns: List[str], max_chars: int = 8000) -> pd.DataFrame:
    out = df.copy()
    out["case_text_for_analysis"] = combine_text_columns(out, text_columns, max_chars=max_chars)
    return out
