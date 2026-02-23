from pathlib import Path
import pandas as pd


from pathlib import Path
import pandas as pd

def write_output_excel(output_path: Path, per_disease_df: pd.DataFrame, per_report_df: pd.DataFrame) -> None:
    
    df = per_disease_df.copy()
    if "disease" in df.columns and "Disease" not in df.columns:
        df = df.rename(columns={"disease": "Disease"})

    required = {"Disease", "TP", "FP", "TN", "FN"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"per_disease_df missing columns: {missing}")

    tp, fp, tn, fn = df["TP"], df["FP"], df["TN"], df["FN"]
    sens = tp / (tp + fn).replace({0: pd.NA})
    spec = tn / (tn + fp).replace({0: pd.NA})
    check = tp + fn + tn + fp
    pos_gt = tp + fn
    neg_gt = tn + fp

    per_disease_df = pd.DataFrame({
        "Disease": df["Disease"],
        "True Positive": tp,
        "False Negative": fn,
        "True Negative": tn,
        "False Positive": fp,
        "Sensitivity": sens,
        "Specificity": spec,
        "Check": check,
        "Positive Ground Truth": pos_gt,
        "Negative Ground Truth": neg_gt,
        "Ground Truth Check": check,
    })


    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        per_disease_df.to_excel(writer, index=False, sheet_name="ConfusionMatrix")
        per_report_df.to_excel(writer, index=False, sheet_name="Predictions")