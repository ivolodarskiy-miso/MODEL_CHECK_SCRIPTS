import sys
import os
sys.path.append(r'/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/runcheck_utils')
from run_checks_util import get_field_namespace
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
def abs_val(x):
    try:
        return abs(float(x))
    except Exception:
        return 0.0

def main():
    if len(sys.argv) != 2:
        print("\nUsage: monelm_exc_check.py dumped_file_prefix\n")
        sys.exit(1)
    prefix =sys.argv[1]

    try:
        LN_KV = open(f"line_kv_{prefix}.csv", "w")
        LN_KV.write("From_CO,FromSt,To_CO,To_ST,Line, LN, ND, ND_KV, ZND, ZND_KV\n")
        LN_RX = open(f"line_rx_{prefix}.csv", "w")
        LN_RX.write("From_CO,FromSt,To_CO,To_ST,Line, LN, R,X\n")
    except IOError as e:
        print(f"Couldn't write to output files: {e}")
        sys.exit(1)

    # Read from existing errors
    line_id = {}
    try:
        with open("existing_line_kv.csv", "r") as exist_kv:
           #next(line)
            for line in exist_kv:
                line = line.rstrip("\n").replace("'", "")
                if not line.strip():
                    continue  # Skip blank lines
                fds = line.split(",")
                key_exist = f"{fds[4]}^{fds[5]}"
                line_id[key_exist] = fds[4]
    except IOError as e:
        print(f"Couldn't read from existing_line_kv.csv file: {e}")
        sys.exit(1)

    line_id_rx = {}
    try:
        with open("existing_RX.csv", "r") as exist_rx:
            for line in exist_rx:
                line = line.rstrip("\n").replace("'", "")
                fds = line.split(",")
                key_exist_rx = f"{fds[4]}^{fds[5]}"
                line_id_rx[key_exist_rx] = fds[4]
    except IOError as e:
        print(f"Couldn't read from existing_RX.csv file: {e}")
        sys.exit(1)

    # Read from nd.csv
    id_nd = {}
    st_nd = {}
    kv_nd = {}
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/nd_{prefix}.csv", "r") as ND:
        #with open(f"nd_{prefix}.csv", "r") as ND:
            nd_idx = get_field_namespace("ND")  # map of field names to indices for ND
            for line in ND:
                line = line.rstrip("\n").replace("'", "")
                fds = line.split(",")
                key = fds[12]
                id_nd[key] = fds[nd_idx.ID_ND]
                st_nd[key] = fds[nd_idx.ID_ST]
                kv_nd[f"{fds[nd_idx.ID_ST]},{fds[nd_idx.ID_ND]}"] = fds[nd_idx.ID_KV]
    except IOError as e:
        print(f"Couldn't read from nd_{prefix}.csv file: {e}")
        sys.exit(1)

    # Read from st.csv
    id_st = {}
    co_st = {}
    dv_st = {}
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/st_{prefix}.csv", "r") as ST:
        #with open(f"st_{prefix}.csv", "r") as ST:
            st_idx = get_field_namespace("ST")  # map of field names to indices for ST
            for line in ST:
                line = line.rstrip("\n").replace("'", "")
                fds = line.split(",")
                key = fds[st_idx.ID_ST]
                id_st[key] = fds[st_idx.ID_ST]
                co_st[key] = fds[st_idx.ID_CO]
                dv_st[f"{fds[st_idx.ID_CO]},{fds[st_idx.ID_ST]}"] = fds[st_idx.ID_DV]
    except IOError as e:
        print(f"Couldn't read from st_{prefix}.csv file: {e}")
        sys.exit(1)

    # Read from ln.csv
    id_ln = {}
    st_ln = {}
    nd_ln = {}
    id_line = {}
    zst_ln = {}
    znd_ln = {}
    r_ln = {}
    x_ln = {}
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv", "r") as LN:
        #with open(f"ln_{prefix}.csv", "r") as LN:
            ln_idx = get_field_namespace("LN")  # map of field names to indices for LN
            for line in LN:
                line = line.rstrip("\n").replace("'", "")
                fds = line.split(",")
                key = fds[8]
                id_ln[key] = fds[ln_idx.ID_LN]#3
                st_ln[key] = fds[ln_idx.ST_LN]#4
                nd_ln[key] = fds[ln_idx.ND_LN]#6
                id_line[key] = fds[ln_idx.ID_LINE]#2
                zst_ln[key] = fds[ln_idx.ZST_LN]#5
                znd_ln[key] = fds[ln_idx.ZND_LN]#7
                r_ln[key] = fds[ln_idx.R]#11
                x_ln[key] = fds[ln_idx.X]#12
                exist_ln = f"{fds[ln_idx.ID_LINE]}^{fds[ln_idx.ID_LN]}"
                # Check for kv mismatch and not in existing errors
                if (
                    float(kv_nd.get(f"{fds[ln_idx.ST_LN]},{fds[ln_idx.ND_LN]}", "")) != float(kv_nd.get(f"{fds[ln_idx.ZST_LN]},{fds[ln_idx.ZND_LN]}", ""))
                ) and (id_line[key] != line_id.get(exist_ln, "")):
                    LN_KV.write(f"{co_st.get(st_ln[key],'')},{st_ln.get(key,'')},{co_st.get(zst_ln[key],'')},{zst_ln.get(key,'')},{id_line.get(key,'')},{id_ln.get(key,'')},{nd_ln.get(key,'')},{kv_nd.get(f'{fds[ln_idx.ST_LN]},{fds[ln_idx.ND_LN]}','')},{znd_ln.get(key,'')},{kv_nd.get(f'{fds[ln_idx.ZST_LN]},{fds[ln_idx.ZND_LN]}','')}\n")
                
                # Check for R/X > 2 and not in existing RX errors
                try:
                    r_val = abs_val(r_ln[key])
                    x_val = abs_val(x_ln[key])
                    if (x_val != 0) and ((r_val / x_val) > 2) and (id_line[key] != line_id_rx.get(exist_ln, "")):
                        LN_RX.write(f"{co_st.get(st_ln[key],'')},{st_ln.get(key,'')},{co_st.get(zst_ln[key],'')},{zst_ln.get(key,'')},{id_line.get(key,'')},{id_ln.get(key,'')},{r_ln.get(key,'')},{x_ln.get(key,'')}\n")
                except Exception:
                    continue
    except IOError as e:
        print(f"Couldn't read from ln_{prefix}.csv file: {e}")
        sys.exit(1)

    # Read from zbr.csv
    id_zbr = {}
    st_zbr = {}
    nd_zbr = {}
    id_line_zbr = {}
    zst_zbr = {}
    znd_zbr = {}
    try:
        idx_zbr = get_field_namespace("ZBR")  # map of field names to indices for ZBR
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv", "r") as ZBR:
        #with open(f"zbr_{prefix}.csv", "r") as ZBR:
            for line in ZBR:
                line = line.rstrip("\n").replace("'", "")
                fds = line.split(",")
                key = fds[10]
                id_zbr[key] = fds[idx_zbr.ID_ZBR]
                st_zbr[key] = fds[idx_zbr.ST_ZBR]
                nd_zbr[key] = fds[idx_zbr.ND]
                id_line_zbr[key] = fds[idx_zbr.ID_LINE]
                zst_zbr[key] = fds[idx_zbr.ZST_ZBR]
                znd_zbr[key] = fds[idx_zbr.ZND]
                exist_zb = f"{fds[idx_zbr.ID_LINE]}^{fds[idx_zbr.ID_ZBR]}"
                if (float(kv_nd.get(f"{fds[idx_zbr.ST_ZBR]},{fds[idx_zbr.ND]}", "0.0"))) != float(kv_nd.get(f"{fds[idx_zbr.ZST_ZBR]},{fds[idx_zbr.ZND]}", "")) and (id_line_zbr[key] != line_id.get(exist_zb, "0.0")):
                    LN_KV.write(f"{co_st.get(st_zbr[key],'')},{st_zbr.get(key,'')},{co_st.get(zst_zbr[key],'')},{zst_zbr.get(key,'')},{id_line_zbr.get(key,'')},{id_zbr.get(key,'')},{nd_zbr.get(key,'')},{kv_nd.get(f'{fds[idx_zbr.ST_ZBR]},{fds[idx_zbr.ND]}','')},{znd_zbr.get(key,'')},{kv_nd.get(f'{fds[idx_zbr.ZST_ZBR]},{fds[idx_zbr.ZND]}','')}\n")
    except IOError as e:
        print(f"Couldn't read from zbr_{prefix}.csv file: {e}")
        sys.exit(1)

    LN_KV.close()
    LN_RX.close()

if __name__ == "__main__":
    main()

