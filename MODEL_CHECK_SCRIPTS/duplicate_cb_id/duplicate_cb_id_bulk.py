import sys
import csv
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: duplicate_cb_id_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]
    input_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cb_{prefix}.csv"
    output_file = f"duplicate_cb_id_{prefix}.csv"

    if not os.path.exists(input_file):
        print(f"*****ABORT***** Could not read from cb_{prefix}.csv file.\n\n\n")
        sys.exit(1)

    line_count = {}
    duplicates = []

    with open(input_file, newline='', encoding='utf-8') as nu, \
         open(output_file, "w", newline='', encoding='utf-8') as duplist:
        writer = csv.writer(duplist)
        writer.writerow(["CO", "ST", "CBTYP", "CB"])
        for line in nu:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            key = fds[1] + "|" + fds[3]
            line_count[key] = line_count.get(key, 0) + 1
            if line_count[key] >= 2:
                row = [fds[12], fds[1], fds[2], fds[3]]
                writer.writerow(row)
                print(",".join(row))

    # Print the output file contents (like `cat` in Perl)
    with open(output_file, encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    main()