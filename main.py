import argparse
import pandas as pd
#from io_excel import write_confusion_matrix

# write the main operation to read and output the confusion matrix
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Input Excel")
    args = parser.parse_args()

    df = pd.read_excel(args.file)

    write_confusion_matrix(df, "confusion_output.xlsx")
    print(" Evaluation complete")


if __name__ == "__main__":
    main()

