from pathlib import Path
import pandas as pd

def write_output_excel(path: Path, per_disease_df: pd.DataFrame, per_report_df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        per_disease_df.to_excel(w, index=False, sheet_name="PerDisease")
        per_report_df.to_excel(w, index=False, sheet_name="PerReport")
