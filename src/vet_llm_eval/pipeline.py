from pathlib import Path
from dotenv import load_dotenv

from vet_llm_eval.excel_processor import read_input_excel, get_disease_columns, ID_COL, TEXT_COLS
from vet_llm_eval.prompts import build_prompt
from vet_llm_eval.llm_gemini import GeminiClient
from vet_llm_eval.parsing import parse_llm_output
from vet_llm_eval.scoring import compute_confusion
from vet_llm_eval.output_excel import write_output_excel

def run_pipeline(
    input_path: Path,
    output_path: Path,
    model: str,
    batch_size: int,
    max_rows: int | None,
    dry_run: bool,
) -> None:
    load_dotenv()  # reads .env if present

    df = read_input_excel(str(input_path))
    if max_rows is not None:
        df = df.head(max_rows).copy()

    diseases = get_disease_columns(df)

    prompts = [build_prompt(row.to_dict(), diseases) for _, row in df.iterrows()]

    if dry_run:
        raw_outputs = ["{}" for _ in prompts]
    else:
        client = GeminiClient(model=model)
        raw_outputs = client.generate_batch(prompts, batch_size=batch_size)

    preds = [parse_llm_output(t, diseases) for t in raw_outputs]

    per_disease_df, per_report_df = compute_confusion(df, preds, diseases)

    
    context_df = df[[ID_COL, *TEXT_COLS]].copy()
    per_report_df = per_report_df.merge(context_df, on=ID_COL, how="left")

    write_output_excel(output_path, per_disease_df, per_report_df)
    print(f"Done. Wrote: {output_path}")
