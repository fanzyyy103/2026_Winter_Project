from __future__ import annotations
import pandas as pd

ID_COL = "CaseID"

TEXT_COLS = [
    "Findings (original radiologist report)",
    "Conclusions (original radiologist report)",
    "Recommendations (original radiologist report)",
]

def read_input_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    missing = [c for c in [ID_COL, *TEXT_COLS] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df[ID_COL].isna().any():
        bad = df[df[ID_COL].isna()].index.tolist()[:10]
        raise ValueError(f"{ID_COL} has missing values at rows: {bad}")

    return df

def get_disease_columns(df: pd.DataFrame) -> list[str]:
    excluded = set([ID_COL, *TEXT_COLS])
    diseases = [c for c in df.columns if c not in excluded]
    if not diseases:
        raise ValueError("No disease columns found.")
    return diseases

