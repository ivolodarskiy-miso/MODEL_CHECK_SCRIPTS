import sys

def main():
    if len(sys.argv) != 2:
        print("\nUsage: TLN_check_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]
    errorout_file = f"TLN_check_{prefix}.txt"
    tln_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/tln_{prefix}.csv"

    try:
        TLN = open(tln_file, encoding="utf-8")
    except Exception:
        print("\n\n\n*****ABORT*****Could not read from tln.csv\n\n\n")
        sys.exit(1)

    errorout = open(errorout_file, "w", encoding="utf-8")

    tln_ID = {}
    i = 0

    for line in TLN:
        line = line.strip().replace("'", "")
        fields = line.split(",")
        i += 1

        if len(fields) > 5 and fields[5] == "0":
            area = fields[1]
            tln = fields[2]
            st = fields[3]
            nd = fields[4]
            tln_key = area + '$' + tln

            # Check for existing TLN ID
            if tln in tln_ID:
                # If st or nd do not match, print both records
                if tln_ID[tln][0] != st or tln_ID[tln][1] != nd:
                    print(f"{i},{tln_ID[tln][2]},{tln_ID[tln][3]},{tln_ID[tln][0]},{tln_ID[tln][1]}")
                    print(f"{i},{area},{tln},{st},{nd}")
                    errorout.write(f"{i},{tln_ID[tln][2]},{tln_ID[tln][3]},{tln_ID[tln][0]},{tln_ID[tln][1]}\n")
                    errorout.write(f"{i},{area},{tln},{st},{nd}\n")
                tln_ID[tln][4] += 1
            else:
                count = 1
                tln_ID[tln] = [st, nd, area, tln, count]

    TLN.close()

    print("\n\nChecking if TLN record is in pairs\n\n")
    errorout.write("\n\nChecking if TLN record is in pairs\n\n")

    for k, v in tln_ID.items():
        if v[4] != 2:
            print(f"{v[2]},{v[3]},{v[0]},{v[1]},count={v[4]}")
            errorout.write(f"{v[2]},{v[3]},{v[0]},{v[1]},count={v[4]}\n")

    errorout.close()

if __name__ == "__main__":
    main()