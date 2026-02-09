import argparse
import pandas as pd
from excel_processor import write_confusion_matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Input Excel")
    args = parser.parse_args()

    df = pd.read_excel(args.file)

    write_confusion_matrix(df, "output/confusion_output.xlsx")
    print(" Evaluation complete")


if __name__ == "__main__":
    main()

