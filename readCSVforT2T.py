import pandas as pd
import sys

def count_rows_with_value_over_50(file_path):
    df = pd.read_csv(file_path)

    column_a = df.iloc[:, 0]
    column_c = df.iloc[:, 2]
    column_d = df.iloc[:, 3]

    contig_names = column_a.str.split('_', expand=True)[0]
    seen_contigs = set()
    c_over_50_flags = []
    d_over_50_flags = []

    for i in range(len(df)):
        contig = contig_names.iloc[i]
        c_val = column_c.iloc[i]
        d_val = column_d.iloc[i]

        if contig in seen_contigs:
            c_over_50_flags.append(False)
            d_over_50_flags.append(False)
        else:
            seen_contigs.add(contig)
            c_over_50_flags.append(c_val > 50)
            d_over_50_flags.append(d_val > 50)


    c_over_50 = pd.Series(c_over_50_flags)
    d_over_50 = pd.Series(d_over_50_flags)

    both_over_50 = (c_over_50 & d_over_50).sum()
    only_c_over_50 = (c_over_50 & ~d_over_50).sum()
    only_d_over_50 = (~c_over_50 & d_over_50).sum()
    either_or_both_over_50 = (c_over_50 | d_over_50).sum()

    return both_over_50, only_c_over_50, only_d_over_50, either_or_both_over_50

def print_results_for_file(file):
    both_over_50, only_c_over_50, only_d_over_50, either_or_both_over_50 = count_rows_with_value_over_50(file)

    print(f"Results for {file}:")
    print(f"Both C and D over 50: {both_over_50}")
    print(f"Only C over 50: {only_c_over_50}")
    print(f"Only D over 50: {only_d_over_50}")
    print(f"Either C or D (or both) over 50: {either_or_both_over_50}")
    print()

def main(file1, file2):
    print_results_for_file(file1)
    print_results_for_file(file2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python readCSVforT2T.py file1.csv file2.csv")
    else:
        main(sys.argv[1], sys.argv[2])
