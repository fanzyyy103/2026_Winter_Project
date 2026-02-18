from __future__ import annotations
import pandas as pd

def normalize_gold(x) -> str:
    if pd.isna(x):
        return "Normal"
    s = str(x).strip().lower()
    if s in {"abnormal", "1", "true", "yes", "positive", "pos"}:
        return "Abnormal"
    return "Normal"

def outcome(gold: str, pred: str) -> str:
    if gold == "Abnormal" and pred == "Abnormal": return "TP"
    if gold == "Normal" and pred == "Abnormal": return "FP"
    if gold == "Normal" and pred == "Normal": return "TN"
    return "FN"

def compute_confusion(df: pd.DataFrame, preds: list[dict], diseases: list[str], id_col: str):
    rows = []
    for i, pred_map in enumerate(preds):
        cid = df.loc[i, id_col]
        for d in diseases:
            g = normalize_gold(df.loc[i, d])
            p = pred_map.get(d, "Normal")
            rows.append({
                "CaseID": cid,
                "row_index": i,
                "disease": d,
                "gold": g,
                "pred": p,
                "outcome": outcome(g, p),
            })

    per_report_df = pd.DataFrame(rows)

    per_disease_df = (
        per_report_df.pivot_table(index="disease", columns="outcome", aggfunc="size", fill_value=0)
        .reset_index()
    )
    for col in ["TP", "FP", "TN", "FN"]:
        if col not in per_disease_df.columns:
            per_disease_df[col] = 0

    per_disease_df = per_disease_df[["disease", "TP", "FP", "TN", "FN"]]
    return per_disease_df, per_report_df
