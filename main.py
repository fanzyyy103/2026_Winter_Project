import argparse
from excel_processor import read_input_excel, write_confusion_matrix
from gemini_client import batch_prompts


def main():
    parser = argparse.ArgumentParser(description="Excel Confusion Matrix Generator")
    parser.add_argument("file", help="Path to input Excel file")
    args = parser.parse_args()

    df = read_input_excel(args.file)

    # Example Gemini usage
    prompts = df["text"].astype(str).tolist()
    gemini_results = batch_prompts(prompts)

    df["gemini_output"] = gemini_results[:len(df)]

    output_path = "output/confusion_output.xlsx"
    write_confusion_matrix(df, output_path)

    print(f" Confusion matrix written to {output_path}")


if __name__ == "__main__":
    main()
