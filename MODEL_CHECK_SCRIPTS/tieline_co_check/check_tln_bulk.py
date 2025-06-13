import sys

def main():
    if len(sys.argv) != 2:
        print("\nUsage: check_tln_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]
    errorout_file = f"tieline_co_check_{prefix}.txt"

    # AREA
    areaid_area = {}
    area_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/area_{prefix}.csv"
    try:
        with open(area_file, encoding="utf-8") as f:
            for line in f:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 2: # ensuring there are enough fiels to not get indexerror
                    areaid_area[fields[1]] = fields[2]
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from area_{prefix}.csv\n\n\n")
        sys.exit(1)

    # LN2
    co1_ln2 = {}
    co2_ln2 = {}
    ln2_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln2_{prefix}.csv"
    try:
        with open(ln2_file, encoding="utf-8") as f:
            for line in f:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 10: # ensuring there are enough fiels to not get indexerror
                    co1_ln2[fields[10]] = fields[7]
                if len(fields) > 7: # ensuring there are enough fiels to not get indexerror
                    co2_ln2[fields[5]] = fields[7]
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from ln2_{prefix}.csv\n\n\n")
        sys.exit(1)

    # ZBR2
    co1_zbr2 = {}
    co2_zbr2 = {}
    zbr2_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr2_{prefix}.csv"
    try:
        with open(zbr2_file, encoding="utf-8") as f:
            for line in f:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 10: # ensuring there are enough fiels to not get indexerror
                    co1_zbr2[fields[10]] = fields[7]
                if len(fields) > 7: # ensuring there are enough fiels to not get indexerror
                    co2_zbr2[fields[5]] = fields[7]
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from zbr2_{prefix}.csv\n\n\n")
        sys.exit(1)

    # LD
    co1_ld = {}
    co2_ld = {}
    ld_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ld_{prefix}.csv"
    try:
        with open(ld_file, encoding="utf-8") as f:
            for line in f:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 21: # ensuring there are enough fiels to not get indexerror
                    co1_ld[fields[16]] = areaid_area.get(fields[20], "")
                    co2_ld[fields[16]] = areaid_area.get(fields[21], "")
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from ld_{prefix}.csv\n\n\n")
        sys.exit(1)

    # TLN
    tln_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/tln_{prefix}.csv"
    try:
        errorout = open(errorout_file, "w", encoding="utf-8")
        with open(tln_file, encoding="utf-8") as f:
            for line in f:
                fields = line.strip().replace("'", "").split(",")
                if len(fields) > 11:
                    area1_tln = areaid_area.get(fields[7], "")
                    tlnid_tln = fields[2]
                    ln2pt_tln = fields[9]
                    zbr2pt_tln = fields[10]
                    ldpt_tln = fields[11]

                    if ln2pt_tln != "0":
                        if area1_tln != co1_ln2.get(ln2pt_tln, "") and area1_tln != co2_ln2.get(ln2pt_tln, ""):
                            msg = (f"ERROR: TLN {tlnid_tln} area id {area1_tln} does not match "
                                   f"Line Modeling company areas {co1_ln2.get(ln2pt_tln, '')} or {co2_ln2.get(ln2pt_tln, '')}\n")
                            print(msg.strip())
                            errorout.write(msg)
                    elif zbr2pt_tln != "0":
                        if area1_tln != co1_zbr2.get(zbr2pt_tln, "") and area1_tln != co2_zbr2.get(zbr2pt_tln, ""):
                            msg = (f"ERROR: TLN {tlnid_tln} area id {area1_tln} does not match "
                                   f"ZBR Modeling company areas {co1_zbr2.get(zbr2pt_tln, '')} or {co2_zbr2.get(zbr2pt_tln, '')}\n")
                            print(msg.strip())
                            errorout.write(msg)
                    elif ldpt_tln != "0":
                        #--------------------------------------------------------------------------------------------------------------
                        #  Don't need to check for Pseudo_tied Loads being in a different CO than one of the ST/ZST CO
                        #  Pavan - 08012023
                        #-----------------------------------------------------------------------------------------
                        pass
                    else:
                        msg = (f"ERROR: TLN {tlnid_tln} area id {area1_tln} is not modeled as a Load, Line, or ZBR\n")
                        print(msg.strip())
                        errorout.write(msg)
        errorout.close()
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from tln_{prefix}.csv\n\n\n")
        sys.exit(1)

if __name__ == "__main__":
    main()