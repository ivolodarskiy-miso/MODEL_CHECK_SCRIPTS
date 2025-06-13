import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: line_in_wrong_dv_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Read ST file
    dv_stn = {}
    st = {}
    st_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/st_{prefix}.csv"
    try:
        with open(st_file, encoding="utf-8") as STN:
            for line in STN:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                if len(fds) > 3:
                    stn_key = fds[3]
                    dv_stn[stn_key] = fds[2]
                    st[stn_key] = fds[3]
    except Exception:
        print(f"Could not read from st_{prefix}.csv file\n\n\n")
        sys.exit(1)

    # Prepare output file
    out_file = f"lines_in_wrong_dv_{prefix}.csv"
    try:
        xdv = open(out_file, "w", encoding="utf-8")
    except Exception:
        print(f"Could not write to lines_in_wrong_dv_{prefix}.csv file\n\n\n\n")
        sys.exit(1)
    xdv.write("Line_CO,Line_DV,LINE,LN,ST,ST_DV,ND,ZST,ZST_DV,ZND,R,X,BCH\n")

    # Read LN file
    ln_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv"
    try:
        with open(ln_file, encoding="utf-8") as LIN:
            for line in LIN:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                if len(fds) > 13:
                    key_ln = fds[8]
                    st_ln = fds[4]
                    zst_ln = fds[5]
                    dv_ln = fds[10]
                    if dv_ln != dv_stn.get(st_ln, "") and dv_ln != dv_stn.get(zst_ln, ""):
                        xdv.write(f"{fds[1]},{fds[10]},{fds[2]},{fds[3]},{fds[4]},{dv_stn.get(st_ln, '')},{fds[6]},{fds[5]},{dv_stn.get(zst_ln, '')},{fds[7]},{fds[11]},{fds[12]},{fds[13]}\n")
    except Exception:
        print(f"Could not read from ln_{prefix}.csv file\n\n\n")
        xdv.close()
        sys.exit(1)

    # Read ZBR file
    zbr_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv"
    try:
        with open(zbr_file, encoding="utf-8") as ZBR:
            for line in ZBR:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                if len(fds) > 14:
                    st_zbr = fds[7]
                    zst_zbr = fds[8]
                    dv_zbr = fds[12]
                    if dv_zbr != dv_stn.get(st_zbr, "") and dv_zbr != dv_stn.get(zst_zbr, ""):
                        xdv.write(f"{fds[9]},{fds[12]},{fds[1]},{fds[2]},{fds[7]},{dv_stn.get(st_zbr, '')},{fds[13]},{fds[8]},{dv_stn.get(zst_zbr, '')},{fds[14]}\n")
    except Exception:
        print(f"Could not read from zbr_{prefix}.csv file\n\n\n")
        xdv.close()
        sys.exit(1)

    xdv.close()

    # Print the output file contents (like `cat`)
    with open(out_file, encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    main()