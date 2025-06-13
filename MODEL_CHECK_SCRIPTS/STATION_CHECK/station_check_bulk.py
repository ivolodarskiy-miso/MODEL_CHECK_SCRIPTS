import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: station_check_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    out_file = f"ST_NEW_{prefix}"
    st_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/st_{prefix}.csv"

    try:
        with open(st_file, encoding="utf-8") as st, open(out_file, "w", encoding="utf-8") as stn:
            for line in st:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                if len(fds) > 3:
                    stn.write(f"{fds[0]},{fds[1]},{fds[3]}\n")
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from st_{prefix}.csv\n\n\n")
        sys.exit(1)

    # Run the shell script as in Perl
    os.system(f"csh -f station_check_bulk.csh {prefix}")

if __name__ == "__main__":
    main()