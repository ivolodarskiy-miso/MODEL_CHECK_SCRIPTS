import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: childless_eq.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    duplicate_file = f"childless_equipment_{prefix}.csv"
    dupl_script_file = f"rem_cbtyp_childless_{prefix}.rio"

    cb_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cb_{prefix}.csv"
    cbtyp_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cbtyp_{prefix}.csv"

    cbtype = {}

    # Read CB file and build cbtype keys
    try:
        with open(cb_file, encoding="utf-8") as br:
            for line in br:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 12:
                    key = fields[12] + "|" + fields[1] + "|" + fields[2]
                    cbtype[key] = 1
    except Exception:
        print(f"\n\n\n*****ABORT Could not read from {cb_file}*****\n\n\n")
        sys.exit(1)

    # Check CBTYPs for missing children
    try:
        DUPLICATE = open(duplicate_file, "w", encoding="utf-8")
        DUPL_SCRIPT = open(dupl_script_file, "w", encoding="utf-8")
        with open(cbtyp_file, encoding="utf-8") as ln:
            for line in ln:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 3:
                    co = fields[1]
                    st = fields[2]
                    cbtyp = fields[3]
                    key2 = co + "|" + st + "|" + cbtyp
                    if key2 not in cbtype:
                        DUPLICATE.write(f"{co},{st},{cbtyp}\n")
                        DUPL_SCRIPT.write(f'find co="{co}",st="{st}",cbtyp="{cbtyp}";del -y;\n')
                        cbtype[key2] = 1
        DUPLICATE.close()
        DUPL_SCRIPT.close()
    except Exception:
        print(f"\n\n\n*****ABORT Could not read from {cbtyp_file}*****\n\n\n")
        sys.exit(1)

    # Remove the duplicate CSV file as in Perl
    try:
        os.remove(duplicate_file)
    except Exception:
        pass

    print(f" If you are an integrator please check this file during integration ... cleanup_rio/rem_cbtyp_childless_{prefix}.rio ")

if __name__ == "__main__":
    main()