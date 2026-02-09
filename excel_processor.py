import pandas as pd
from openpyxl.styles import Alignment, Font
from openpyxl import load_workbook


def read_input_excel(path: str) -> pd.DataFrame:
    return pd.read_excel(path)


def write_confusion_matrix(df: pd.DataFrame, output_path: str):
    """
    Example confusion-matrix-style output:
    Rows = Actual
    Columns = Predicted
    """

    matrix = pd.crosstab(
        df["actual_label"],
        df["predicted_label"],
        rownames=["Actual"],
        colnames=["Predicted"]
    )

    matrix.to_excel(output_path, sheet_name="Confusion Matrix")

    # Styling (adjust to match your example file)
    wb = load_workbook(output_path)
    ws = wb.active

    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")

            if cell.row == 1 or cell.column == 1:
                cell.font = Font(bold=True)

    wb.save(output_path)
