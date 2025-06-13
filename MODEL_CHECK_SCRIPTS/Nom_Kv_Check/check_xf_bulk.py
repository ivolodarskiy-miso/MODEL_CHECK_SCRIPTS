import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: check_xf_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Read existing_xf.csv
    xf_exist = {}
    try:
        with open("existing_xf.csv", encoding="utf-8") as existing:
            for line in existing:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                exist_key = fds[0] + "_" + fds[1] + "_" + fds[2]
                xf_exist[exist_key] = fds[2]
    except Exception:
        pass  # If file doesn't exist, just skip

    # Read ND file and build kv_nd dictionary
    kv_nd = {}
    nd_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/nd_{prefix}.csv"
    try:
        with open(nd_file, encoding="utf-8") as ND:
            for line in ND:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                kv_nd[f"{fds[1]},{fds[4]}"] = float(fds[2])
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from nd_{prefix}.csv\n\n\n")
        sys.exit(1)

    # Open XF file and output file
    xf_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv"
    nom_file = f"Nominal_kv_{prefix}.csv"
    try:
        XF = open(xf_file, encoding="utf-8")
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not read from xf_{prefix}.csv\n\n\n")
        sys.exit(1)
    try:
        nom = open(nom_file, "w", encoding="utf-8")
    except Exception:
        print(f"\n\n\n*****ABORT*****Could not write to Nominal_kv_{prefix}.csv\n\n\n")
        sys.exit(1)

    for line in XF:
        line = line.strip().replace("'", "")
        fds = line.split(",")
        co_xf = fds[7]
        st_xf = fds[1]
        id_xf = fds[2]
        already_exists_key = fds[7] + "_" + fds[1] + "_" + fds[2]
        if id_xf != xf_exist.get(already_exists_key, None):
            # Check ND-KV vs KVNOM
            try:
                nd_kv = kv_nd[f"{fds[1]},{fds[12]}"]
                kvnom = float(fds[26])
                diff = abs((nd_kv - kvnom) * 100 / nd_kv)
                if diff > 15:
                    nom.write(f"CO {fds[7]},ST {fds[1]},ID-XF {fds[2]},ID_ND {fds[12]},KVNOM = {fds[26]},ND-KV = {nd_kv}\n")
            except Exception:
                #General Exception hanling is bad practice but was made to copy legacy perl behavior. It is advised that this get updated to more precisely handle errors
                pass
            # Check ZND-KV vs ZNOMKV
            try:
                znd_kv = kv_nd[f"{fds[1]},{fds[13]}"]
                znokv = float(fds[27])
                diff = abs((znd_kv - znokv) * 100 / znd_kv)
                if diff > 15:
                    nom.write(f"CO {fds[7]},ST {fds[1]},ID-XF {fds[2]},ID_ZND {fds[13]}, ZNOMKV = {fds[27]},ZND-KV = {znd_kv}\n")
            except Exception:
                #General Exception handling is bad practice but was made to copy legacy perl behavior. It is advised that this get updated to more precisely handle errors
                pass

    XF.close()
    nom.close()

    # Print the output file contents (like `cat` in Perl)
    with open(nom_file, encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    main()