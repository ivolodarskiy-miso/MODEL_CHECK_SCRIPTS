import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: monelm_exc_check.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Read existing_dangling.csv
    eq_typ = {}
    area = {}
    st = {}
    eq_name = {}
    try:
        with open("existing_dangling.csv", encoding="utf-8") as DANG:
            for line in DANG:
                fds = line.strip().replace("'", "").split(",")
                key = fds[0] + "^" + fds[2] + "^" + fds[3]
                eq_typ[key] = fds[0]
                area[key] = fds[1]
                st[key] = fds[2]
                if fds[0] in ("LN2", "ZBR2", "XF2"):
                    eq_name[key] = fds[3] + "+++" + fds[4]
                else:
                    eq_name[key] = fds[3]
    except Exception:
        print("Couldn't read from existing_dangling.csv file.\n")
        sys.exit(1)

    new_dang = open(f"new_dangling_equipments_{prefix}.csv", "w", encoding="utf-8")

    # UN
    print("\nprocessing unit data ***\n\n")
    co_un = {}
    st_un = {}
    id_un = {}
    kv_un = {}
    open_un = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/un_{prefix}.csv", encoding="utf-8") as un:
        for line in un:
            fields = line.strip().replace("'", "").split(",")
            key_un = "UN^" + fields[1] + "^" + fields[4]
            co_un[key_un] = fields[6]
            st_un[key_un] = fields[1]
            id_un[key_un] = fields[4]
            kv_un[key_un] = fields[2]
            open_un[key_un] = fields[8]
            if open_un[key_un] == "T" and id_un[key_un] != eq_name.get(key_un, ""):
                print(f"++++++++++++++++++++++++DANGLING UN,{co_un[key_un]},{st_un[key_un]},{id_un[key_un]},{kv_un[key_un]},{fields[11]}")
                new_dang.write(f"UN,{co_un[key_un]},{st_un[key_un]},{id_un[key_un]},{kv_un[key_un]},{fields[11]}\n")

    # LD
    print("processing load data ***\n\n")
    co_ld = {}
    st_ld = {}
    id_ld = {}
    kv_ld = {}
    open_ld = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ld_{prefix}.csv", encoding="utf-8") as ld:
        for line in ld:
            fields = line.strip().replace("'", "").split(",")
            key_ld = "LD^" + fields[1] + "^" + fields[4]
            co_ld[key_ld] = fields[11]
            st_ld[key_ld] = fields[1]
            id_ld[key_ld] = fields[4]
            kv_ld[key_ld] = fields[2]
            open_ld[key_ld] = fields[15]
            if open_ld[key_ld] == "T" and id_ld[key_ld] != eq_name.get(key_ld, ""):
                print(f"++++++++++++++++++++++++DANGLING LD,{co_ld[key_ld]},{st_ld[key_ld]},{id_ld[key_ld]},{kv_ld[key_ld]},{fields[17]}")
                new_dang.write(f"LD,{co_ld[key_ld]},{st_ld[key_ld]},{id_ld[key_ld]},{kv_ld[key_ld]},{fields[17]}\n")

    # CP
    print("processing CP data ***\n\n")
    co_cp = {}
    st_cp = {}
    id_cp = {}
    kv_cp = {}
    open_cp = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cp_{prefix}.csv", encoding="utf-8") as cp:
        for line in cp:
            fields = line.strip().replace("'", "").split(",")
            key_cp = "CP^" + fields[1] + "^" + fields[4]
            co_cp[key_cp] = fields[6]
            st_cp[key_cp] = fields[1]
            id_cp[key_cp] = fields[4]
            kv_cp[key_cp] = fields[2]
            open_cp[key_cp] = fields[8]
            if open_cp[key_cp] == "T" and id_cp[key_cp] != eq_name.get(key_cp, "") and id_cp[key_cp] != "PSEUDO":
                print(f"++++++++++++++++++++++++DANGLING CP,{co_cp[key_cp]},{st_cp[key_cp]},{id_cp[key_cp]},{kv_cp[key_cp]},{fields[9]}")
                new_dang.write(f"CP,{co_cp[key_cp]},{st_cp[key_cp]},{id_cp[key_cp]},{kv_cp[key_cp]},{fields[9]}\n")

    # ZBR
    print("processing zbr data ***\n\n")
    id_zbr = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv", encoding="utf-8") as zbr:
        for line in zbr:
            fields = line.strip().replace("'", "").split(",")
            key_zbr = fields[10]
            id_zbr[key_zbr] = fields[2]

    # LN
    print("processing Ln data ***\n\n")
    id_ln = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv", encoding="utf-8") as ln:
        for line in ln:
            fields = line.strip().replace("'", "").split(",")
            key_ln = fields[8]
            id_ln[key_ln] = fields[3]

    # LN2
    print("processing Line data ***\n\n")
    co_ln2 = {}
    st_ln2 = {}
    id_ln2 = {}
    subscript_ln = {}
    kv_ln2 = {}
    nd_ln2 = {}
    open_ln2 = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln2_{prefix}.csv", encoding="utf-8") as ln2:
        for line in ln2:
            fields = line.strip().replace("'", "").split(",")
            key_ln2 = "LN2^" + fields[2] + "^" + fields[1]
            co_ln2[key_ln2] = fields[7]
            st_ln2[key_ln2] = fields[2]
            id_ln2[key_ln2] = fields[1]
            subscript_ln[key_ln2] = fields[6]
            kv_ln2[key_ln2] = fields[3]
            nd_ln2[key_ln2] = fields[11]
            open_ln2[key_ln2] = fields[9]
            ln_ln2 = id_ln.get(fields[6], "")
            ln2ln = fields[1] + "+++" + ln_ln2
            if open_ln2[key_ln2] == "T" and ln2ln != eq_name.get(key_ln2, ""):
                print(f"++++++++++++++++++++++++DANGLING LN2,{co_ln2[key_ln2]},{st_ln2[key_ln2]},{id_ln2[key_ln2]},{ln_ln2},{kv_ln2[key_ln2]},{nd_ln2[key_ln2]}\n\n\n")
                new_dang.write(f"LN2,{co_ln2[key_ln2]},{st_ln2[key_ln2]},{id_ln2[key_ln2]},{ln_ln2},{kv_ln2[key_ln2]},{nd_ln2[key_ln2]}\n")

    # ZBR2
    print("processing ZBR2 data ***\n\n")
    co_zbr2 = {}
    st_zbr2 = {}
    id_zbr2 = {}
    subscript_zbr = {}
    kv_zbr2 = {}
    nd_zbr2 = {}
    open_zbr2 = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr2_{prefix}.csv", encoding="utf-8") as zbr2:
        for line in zbr2:
            fields = line.strip().replace("'", "").split(",")
            key_zbr2 = "ZBR2^" + fields[2] + "^" + fields[1]
            co_zbr2[key_zbr2] = fields[7]
            st_zbr2[key_zbr2] = fields[2]
            id_zbr2[key_zbr2] = fields[1]
            subscript_zbr[key_zbr2] = fields[6]
            kv_zbr2[key_zbr2] = fields[3]
            nd_zbr2[key_zbr2] = fields[11]
            open_zbr2[key_zbr2] = fields[9]
            zbr_zbr2 = id_zbr.get(fields[6], "")
            zbr2zbr = fields[1] + "+++" + zbr_zbr2
            # Use LN2 context for output, as in Perl
            key_ln2 = "LN2^" + fields[2] + "^" + fields[1]
            co_ln2_val = co_ln2.get(key_ln2, "")
            st_ln2_val = st_ln2.get(key_ln2, "")
            id_ln2_val = id_ln2.get(key_ln2, "")
            ln_ln2_val = id_ln.get(fields[6], "")
            kv_ln2_val = kv_ln2.get(key_ln2, "")
            nd_ln2_val = nd_ln2.get(key_ln2, "")
            if open_zbr2[key_zbr2] == "T" and zbr2zbr != eq_name.get(key_zbr2, ""):
                print(f"++++++++++++++++++++++++DANGLING ZBR2,{co_zbr2[key_zbr2]},{st_zbr2[key_zbr2]},{id_zbr2[key_zbr2]},{zbr_zbr2},{kv_zbr2[key_zbr2]},{nd_zbr2[key_zbr2]}")
                new_dang.write(f"LN2,{co_ln2_val},{st_ln2_val},{id_ln2_val},{ln_ln2_val},{kv_ln2_val},{nd_ln2_val}\n")

    # XF
    print("processing XF data ***\n\n")
    id_xf = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv", encoding="utf-8") as xf:
        for line in xf:
            fields = line.strip().replace("'", "").split(",")
            key_xf = fields[9]
            id_xf[key_xf] = fields[2]

    # XF2
    print("processing Xfmr data ***\n\n")
    co_xf2 = {}
    st_xf2 = {}
    id_xf2 = {}
    subscript_xf = {}
    kv_xf2 = {}
    nd_xf2 = {}
    open_xf2 = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf2_{prefix}.csv", encoding="utf-8") as xf2:
        for line in xf2:
            fields = line.strip().replace("'", "").split(",")
            key_xf2 = "XF2^" + fields[2] + "^" + fields[1]
            co_xf2[key_xf2] = fields[7]
            st_xf2[key_xf2] = fields[2]
            id_xf2[key_xf2] = fields[1]
            subscript_xf[key_xf2] = fields[6]
            kv_xf2[key_xf2] = fields[3]
            nd_xf2[key_xf2] = fields[10]
            open_xf2[key_xf2] = fields[9]
            xf_xf2 = id_xf.get(fields[6], "")
            xf2xf = fields[1] + "+++" + xf_xf2
            if open_xf2[key_xf2] == "T" and xf2xf != eq_name.get(key_xf2, ""):
                print(f"++++++++++++++++++++++++DANGLING XF2,{co_xf2[key_xf2]},{st_xf2[key_xf2]},{id_xf2[key_xf2]},{xf_xf2},{kv_xf2[key_xf2]},{nd_xf2[key_xf2]}\n\n\n")
                new_dang.write(f"XF2,{co_xf2[key_xf2]},{st_xf2[key_xf2]},{id_xf2[key_xf2]},{xf_xf2},{kv_xf2[key_xf2]},{nd_xf2[key_xf2]}\n")

    # SVS
    print("\nprocessing svs data ***\n\n")
    co_svs = {}
    st_svs = {}
    id_svs = {}
    kv_svs = {}
    open_svs = {}
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/svs_{prefix}.csv", encoding="utf-8") as svs:
        for line in svs:
            fields = line.strip().replace("'", "").split(",")
            key_svs = "SVS^" + fields[1] + "^" + fields[4]
            co_svs[key_svs] = fields[6]
            st_svs[key_svs] = fields[1]
            id_svs[key_svs] = fields[4]
            kv_svs[key_svs] = fields[2]
            open_svs[key_svs] = fields[8]
            if open_svs[key_svs] == "T" and id_svs[key_svs] != eq_name.get(key_svs, ""):
                print(f"++++++++++++++++++++++++DANGLING SVS,{co_svs[key_svs]},{st_svs[key_svs]},{id_svs[key_svs]},{kv_svs[key_svs]},{fields[11]}")
                new_dang.write(f"SVS,{co_svs[key_svs]},{st_svs[key_svs]},{id_svs[key_svs]},{kv_svs[key_svs]},{fields[11]}\n")

    new_dang.close()

if __name__ == "__main__":
    main()