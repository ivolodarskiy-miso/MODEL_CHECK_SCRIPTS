import sys
import csv
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: unit_regnd.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Output files
    rio_file = f"rio_regnd_{prefix}.rio"
    out_file = f"unit_regnd_{prefix}.csv"
    out1_file = f"unit_vtarget_{prefix}.csv"
    ext_area_file = f"ext_area_{prefix}.csv"

    # Input files
    nd_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/nd_{prefix}.csv"
    area_file = "/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/AREA_UPDATE/area_flags_RTO.csv"
    un_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/un_{prefix}.csv"

    # Read ND file
    id_nd = {}
    st_nd = {}
    kv_nd = {}
    with open(nd_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            key = fds[12]
            id_nd[key] = fds[5]
            st_nd[key] = fds[1]
            kv_nd["{},{}".format(fds[1], fds[5])] = fds[2]

    # Read area_flags_RTO.csv and write ext_area_file
    area = {}
    with open(area_file, encoding='utf-8') as all_areas, \
         open(ext_area_file, "w", encoding='utf-8') as out_:
        for line in all_areas:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            area_id = fds[0]
            region = fds[5]
            if region in ("EXTERNAL", "FT_EAST", "FT_CNTR", "FT_WEST", "FT_SUTH"):
                out_.write(f"{area_id}\n")
    # Read ext_area_file into area dict
    with open(ext_area_file, encoding='utf-8') as f:
        for line in f:
            key_area = line.strip().split(",")[0]
            area[key_area] = key_area

    # Prepare output files
    rio = open(rio_file, "w", encoding='utf-8')
    rio.write("echo -c ON;\n")
    out = open(out_file, "w", encoding='utf-8')
    out.write("CO,ST,UN,ND,REGND\n")
    out1 = open(out1_file, "w", encoding='utf-8')
    out1.write("CO,ST,UN,ND,VTARGET\n")

    # Read UN file and process
    with open(un_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            key = fds[6]
            co_un = fds[6]
            dv_un = fds[10]
            st_un = fds[1]
            id_un = fds[4]
            nd_un = fds[11]
            regnd_un = fds[12]
            vatarget_un = fds[13]
            # For units in external area filter out units where regnd KV not equal to unit nd KV
            if co_un in area and nd_un != regnd_un:
                _rio = f'find st="{st_un}",UN = "{id_un}";/regnd = "{nd_un}";'
                rio.write(f"{_rio}\n")
                rio.write(f"//{co_un},old regnd = {regnd_un}\n")
                out.write(f"{co_un},{st_un},{id_un},{nd_un},{regnd_un}\n")
            # For units if the target voltage is more than 1.1 or less than or equal to 0.9
            try:
                vtarget = float(vatarget_un)
                if vtarget > 1.1 or vtarget <= 0.9:
                    out1.write(f"{co_un},{st_un},{id_un},{nd_un},{regnd_un} ====> has suspect vtarget {vatarget_un}\n")
            except ValueError as e:
                pass  # skip if vatarget_un is not a number

    rio.close()
    out.close()
    out1.close()

    # # Remove temp files
    # try:
    #     os.remove(ext_area_file)
    #     os.remove(out_file)
    # except Exception:
    #     pass

    print(f" If you are an integrator please check this file during integration ... cleanup_rio/rio_regnd_{prefix}.rio ")

if __name__ == "__main__":
    main()