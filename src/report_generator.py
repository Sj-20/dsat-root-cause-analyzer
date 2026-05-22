import io
import pandas as pd

def to_excel_bytes(df: pd.DataFrame, summary_text: str = "") -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Analyzed Cases", index=False)
        summary_df = pd.DataFrame({"Executive Summary": summary_text.split("\n")})
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        root = df["root_cause_category"].value_counts().reset_index()
        root.columns = ["Root Cause", "Count"]
        root.to_excel(writer, sheet_name="Root Cause Summary", index=False)
    return output.getvalue()
