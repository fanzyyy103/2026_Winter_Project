import argparse
from pathlib import Path
from vet_llm_eval.pipeline import run_pipeline

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vet_llm_eval")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run LLM labeling + confusion matrix")
    run.add_argument("--input", required=True, help="Input Excel path")
    run.add_argument("--output", required=True, help="Output Excel path")
    run.add_argument("--model", default="gpt-5-nano-2025-08-07")
    run.add_argument("--batch-size", type=int, default=6)
    run.add_argument("--max-rows", type=int, default=None)
    run.add_argument("--dry-run", action="store_true", help="Skip LLM calls (debug pipeline)")
    run.add_argument("--provider", choices=["openai", "gemini", "mock"], default="openai")


    return p

def main():
    args = build_parser().parse_args()
    if args.cmd == "run":
        run_pipeline(
            input_path=Path(args.input),
            output_path=Path(args.output),
            model=args.model,
            batch_size=args.batch_size,
            max_rows=args.max_rows,
            dry_run=args.dry_run,
            provider=args.provider,
        )
