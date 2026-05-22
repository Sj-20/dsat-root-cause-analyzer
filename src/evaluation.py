import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def evaluate_predictions(df: pd.DataFrame, actual_col: str = "human_label", pred_col: str = "dsat_type") -> dict:
    if actual_col not in df.columns or pred_col not in df.columns:
        return {"error": f"Required columns not found: {actual_col}, {pred_col}"}

    valid = df[[actual_col, pred_col]].dropna()
    if len(valid) == 0:
        return {"error": "No valid rows for evaluation."}

    y_true = valid[actual_col].astype(str)
    y_pred = valid[pred_col].astype(str)

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "labels": sorted(list(set(y_true) | set(y_pred))),
    }
