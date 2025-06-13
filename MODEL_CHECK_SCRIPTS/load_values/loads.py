import sys
import os
sys.path.append(r'/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/runcheck_utils')
from run_checks_util import get_field_namespace

def main():
    if len(sys.argv) != 2:
        print("\nUsage: loads.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    ld_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ld_{prefix}.csv"
    rio_file = f"rio_ld_{prefix}.rio"
    ol_file = f"output_list_{prefix}.csv"

    try:
        LD = open(ld_file, encoding="utf-8")
    except Exception:
        print(f"Could not read from ld_{prefix} file\n\n")
        sys.exit(1)

    RIO = open(rio_file, "w", encoding="utf-8")
    OL = open(ol_file, "w", encoding="utf-8")

    ld_idx = get_field_namespace("LD")
    for line in LD:
        line = line.strip().replace("'", "")
        fds = line.split(",")
        if len(fds) < 20:
            continue  # skip incomplete lines (shouldn't really happen)
        id_ld = fds[ld_idx.ID_LD]
        st_ld = fds[ld_idx.ID_ST]
        wmn_ld = fds[ld_idx.WMN]

        try:
            if wmn_ld =='':
                print(f"WARNING missing wmn_ld value on id_ld: {id_ld}, st_ld: {st_ld}, treating as 0.0")
                wmn_ld = 0.0
            wmn_val = float(wmn_ld)
        except Exception:
            continue

        if -0.01 <= wmn_val <= 0.01 and wmn_val != -0.001:
            OL.write(f"{st_ld},{id_ld},{wmn_ld}\n")
            _rio = f'find st="{fds[1]}",LD = "{fds[4]}";/WMN = -0.001;'
            RIO.write(f"{_rio}\n")
            RIO.write(f"//OLD wmn ==> {wmn_ld}\n")

    print(f" If you are an integrator please check this file during integration ... cleanup_rio/rio_ld_{prefix}.rio ")

    LD.close()
    RIO.close()
    OL.close()

    try:
        os.remove(ol_file)
    except Exception:
        pass

if __name__ == "__main__":
    main()