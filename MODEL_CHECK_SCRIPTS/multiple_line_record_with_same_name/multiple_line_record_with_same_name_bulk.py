import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: multiple_line_record_with_same_name_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Step 1: Read line_$prefix.csv and collect line IDs
    lineid = {}
    line_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/line_{prefix}.csv"
    out_file = f"out_{prefix}.txt"
    with open(line_file, encoding='utf-8') as rline, open(out_file, "w", encoding='utf-8') as out:
        for line in rline:
            line = line.strip().replace("'", "")
            fields = line.split(",")
            key_line = fields[3]
            lineid[key_line] = fields[2]
            out.write(f"{lineid[key_line]}\n")

    # Step 2: Sort and find duplicate line IDs
    outnew_file = f"outnew_{prefix}.txt"
    outnew2_file = f"outnew2_{prefix}.csv"
    with open(out_file, encoding='utf-8') as infile:
        lines = sorted([l.strip() for l in infile if l.strip()])
    with open(outnew_file, "w", encoding='utf-8') as outfile:
        for l in lines:
            outfile.write(l + "\n")
    # Find duplicates (like `uniq -d`)
    from collections import Counter
    counts = Counter(lines)
    duplicates = [item for item, count in counts.items() if count > 1]
    with open(outnew2_file, "w", encoding='utf-8') as out2:
        for dup in duplicates:
            out2.write(dup + "\n")

    # Step 3: Read duplicate line IDs into repeat_lineid
    repeat_lineid = {}
    with open(outnew2_file, encoding='utf-8') as out2:
        for line in out2:
            key_lineid = line.strip()
            if key_lineid:
                repeat_lineid[key_lineid] = key_lineid

    # Step 4: Process LN file
    fin_file = f"multiple_{prefix}.csv"
    with open(fin_file, "w", encoding='utf-8') as fin:
        ln_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv"
        with open(ln_file, encoding='utf-8') as ln_rec:
            for line in ln_rec:
                line = line.strip().replace("'", "")
                fields = line.split(",")
                key = fields[8]
                id_line = fields[2]
                id_ln = fields[3]
                id_co = fields[1]
                id_dv = fields[10]
                st = fields[4]
                nd = fields[6]
                zst = fields[5]
                znd = fields[7]
                R = fields[11]
                X = fields[12]
                BCH = fields[13]
                if id_line == repeat_lineid.get(id_line):
                    fin.write(f"{id_line},{id_ln},{id_co},{id_dv},{st},{nd},{zst},{znd},{R},{X},{BCH}\n")

        # Step 5: Process ZBR file
        zbr_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv"
        with open(zbr_file, encoding='utf-8') as zbr_rec:
            for line in zbr_rec:
                line = line.strip().replace("'", "")
                fields = line.split(",")
                key = fields[10]
                id_line = fields[1]
                id_ln = fields[2]
                id_co = fields[9]
                id_dv = fields[12]
                st = fields[7]
                nd = fields[13]
                zst = fields[8]
                znd = fields[14]
                if id_line == repeat_lineid.get(id_line):
                    fin.write(f"{id_line},{id_ln},{id_co},{id_dv},{st},{nd},{zst},{znd}\n")

    # Step 6: Sort and write final output
    final_csv = f"multiple_line_record_with_same_name_{prefix}.csv"
    with open(fin_file, encoding='utf-8') as fin:
        lines = sorted([l.strip() for l in fin if l.strip()])
    with open(final_csv, "w", encoding='utf-8') as fout:
        for l in lines:
            fout.write(l + "\n")

    # Step 7: Clean up temp files
    for fname in [out_file, outnew_file, outnew2_file, fin_file]:
        try:
            os.remove(fname)
        except Exception:
            pass

    # Step 8: Print the final output (like `cat`)
    with open(final_csv, encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    main()