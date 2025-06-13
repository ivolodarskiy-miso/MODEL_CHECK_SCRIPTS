import sys

def main():
    if len(sys.argv) != 2:
        print("\nUsage: monelm_exc_check.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Read ST file and build st_list
    st_list = {}
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/st_{prefix}.csv", encoding="utf-8") as stf:
            for line in stf:
                line = line.strip().replace("'", "")
                fields = line.split(",")
                if len(fields) > 3:
                    co_st = fields[1]
                    id_st = fields[3]
                    st_list[id_st] = co_st
    except Exception:
        print("*****ABORT***** Could not read from ST file\n\n\n")
        sys.exit(1)

    print("line list\n\n\n")

    try:
        outfile = open(f"CO_LINE_CHECK_{prefix}.csv", "w", encoding="utf-8")
    except Exception:
        print("*****ABORT***** Could not open output file\n\n\n")
        sys.exit(1)

    # Process LN file
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv", encoding="utf-8") as lnf:
            for line in lnf:
                line = line.strip().replace("'", "")
                fields = line.split(",")
                if len(fields) > 5:
                    co_ln = fields[1]
                    id_line = fields[2]
                    id_ln = fields[3]
                    st_line = fields[4]
                    zst_line = fields[5]
                    st_co = st_list.get(st_line, "")
                    zst_co = st_list.get(zst_line, "")
                    if (co_ln != st_co) and (co_ln != zst_co):
                        outstr = f"{co_ln}, {id_line}, {id_ln}, {st_co}, {st_line}, {zst_co}, {zst_line}\n"
                        print(outstr.strip())
                        outfile.write(outstr)
    except Exception:
        print("*****ABORT***** Could not read from LN file\n\n\n")
        outfile.close()
        sys.exit(1)

    print("\n\n\n")
    print("zbr list\n\n\n")

    # Process ZBR file
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv", encoding="utf-8") as zbrf:
            for line in zbrf:
                line = line.strip().replace("'", "")
                fields = line.split(",")
                if len(fields) > 9:
                    co_zbr = fields[9]
                    id_zbr_line = fields[1]
                    id_zbr = fields[2]
                    st_zbr = fields[7]
                    zst_zbr = fields[8]
                    st_co = st_list.get(st_zbr, "")
                    zst_co = st_list.get(zst_zbr, "")
                    if (co_zbr != st_co) and (co_zbr != zst_co):
                        outstr = f"{co_zbr}, {id_zbr_line}, {id_zbr}, {st_co}, {st_zbr}, {zst_co}, {zst_zbr}\n"
                        print(outstr.strip())
                        outfile.write(outstr)
    except Exception:
        print("*****ABORT***** Could not read from zbr.csv\n\n\n")
        outfile.close()
        sys.exit(1)

    print("\n\n\n")
    outfile.close()

if __name__ == "__main__":
    main()