import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: special_char_check.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]
    out_file = f"NETMOM_{prefix}"

    # List of (filename, column indices to print)
    files_and_cols = [
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cb_{prefix}.csv",    [0, 13, 3]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cp_{prefix}.csv",    [0, 11, 4]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv",   [0, 10, 2]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv",    [0, 8, 3]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/line_{prefix}.csv",  [0, 3, 2]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ld_{prefix}.csv",    [0, 16, 4]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/nd_{prefix}.csv",    [0, 12, 4]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/un_{prefix}.csv",    [0, 9, 4]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xfmr_{prefix}.csv",  [0, 4, 3]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv",    [0, 9, 2]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ps_{prefix}.csv",    [0, 1, 2]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/co_{prefix}.csv",    [0, 2, 1]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/dv_{prefix}.csv",    [0, 1, 2]),
        (f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/area_{prefix}.csv",  [0, 1, 2]),
    ]

    try:
        out = open(out_file, "w", encoding="utf-8")
    except Exception:
        print("\n\n\n*****ABORT***** Could not write to NETMOM file\n\n\n")
        sys.exit(1)

    for fname, cols in files_and_cols:
        try:
            with open(fname, encoding="utf-8") as f:
                for line in f:
                    line = line.strip().replace("'", "")
                    fds = line.split(",")
                    # Only print if all columns exist in the row
                    if all(idx < len(fds) for idx in cols):
                        out.write(f"{fds[cols[0]]} {fds[cols[1]]}  {fds[cols[2]]}\n")
        except Exception:
            print(f"\n\n\n*****ABORT***** Could not read from {os.path.basename(fname)}\n\n\n")
            continue

    out.close()

    # Run the shell script as in Perl
    os.system(f"csh -f special_check_bulk.csh {prefix}")

if __name__ == "__main__":
    main()