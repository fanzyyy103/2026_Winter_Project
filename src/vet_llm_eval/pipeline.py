from __future__ import annotations

from pathlib import Path

from vet_llm_eval.io_excel import (
    read_input_excel,
    get_disease_columns,
    ID_COL,
    TEXT_COLS,
)
from vet_llm_eval.scoring import compute_confusion
from vet_llm_eval.output_excel import write_output_excel

from vet_llm_eval.prompt import build_prompt
from vet_llm_eval.parsing import parse_llm_output

from vet_llm_eval.llm_openai import OpenAIClient
from vet_llm_eval.llm_gemini import GeminiClient


def run_pipeline(
    input_path: Path,
    output_path: Path,
    model: str,
    batch_size: int,
    max_rows: int | None,
    dry_run: bool,
    provider: str = "openai",
) -> None:
    """
    Main pipeline:
    1) Read Excel
    2) Detect disease columns
    3) Call LLM (OpenAI or Gemini)
    4) Parse output
    5) Compute confusion matrix
    6) Write Excel output
    """

    # -------------------------
    # 1) Load Excel
    # -------------------------
    df = read_input_excel(str(input_path))

    if max_rows is not None:
        df = df.head(max_rows).copy()

    diseases = get_disease_columns(df)

    print(f"[INFO] Rows: {len(df)}")
    print(f"[INFO] Disease count: {len(diseases)}")
    print(f"[INFO] Provider: {provider}")
    print(f"[INFO] Model: {model}")
    print(f"[INFO] DryRun: {dry_run}")
    print(f"[INFO] Batch size: {batch_size}")

    # -------------------------
    # 2) Generate predictions
    # -------------------------
    preds: list[dict[str, str]] = []

    if dry_run:
        # For scaffolding test only
        preds = [{d: "Normal" for d in diseases} for _ in range(len(df))]
        print("[INFO] Using DRY RUN (all Normal predictions).")

    else:
        # Build prompts
        prompts = [build_prompt(row.to_dict(), diseases) for _, row in df.iterrows()]

        # Choose provider
        if provider == "openai":
            client = OpenAIClient(model=model)
        elif provider == "gemini":
            client = GeminiClient(model=model)
        else:
            raise ValueError("Provider must be 'openai' or 'gemini'")

        print(f"[INFO] Calling {provider}...")
        raw_outputs = client.generate_batch(prompts, batch_size=batch_size)

        # Parse structured output
        preds = [parse_llm_output(text, diseases) for text in raw_outputs]

        print("[INFO] LLM calls complete.")

    # -------------------------
    # 3) Compute confusion matrix
    # -------------------------
    per_disease_df, per_report_df = compute_confusion(
        df=df,
        preds=preds,
        diseases=diseases,
        id_col=ID_COL,
    )

    # Add context for audit
    context_cols = [ID_COL, *TEXT_COLS]
    context = df[context_cols].copy()

    per_report_df = per_report_df.merge(context, on=ID_COL, how="left")

    # -------------------------
    # 4) Write Excel output
    # -------------------------
    write_output_excel(output_path, per_disease_df, per_report_df)

    print(f"[SUCCESS] Output written to: {output_path}")
