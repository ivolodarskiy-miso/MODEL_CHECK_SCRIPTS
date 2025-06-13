import sys
import os
from collections import defaultdict
sys.path.append(r'/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/runcheck_utils')
from run_checks_util import get_field_namespace

#----Objective of script is to get list of CB which have only CP connected to either ND or ZND of the CB
#----Get nodes connected to CP
#----Get nodes connected to LD and UN
#----If UN or LD node is same as CP node add that node to exception list
#----Get nodes connected to line and XF
#----If line or XF nd (or ZND) is same as CP node add that node to exception list
#----Get CB ND and ZND 
#----if there is more than one cb connected to CP then add that node to exception list
#----get all the cb connected to CP except for those in exception list
#----set the cb_cp and cbtyp_cp flag 

def main():
    if len(sys.argv) != 2:
        print("\nUsage: multiple_line_record_with_same_name.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Run the un_ld.csh script
    os.system(f"csh -f un_ld.csh {prefix}")

    # Prepare data structures
    nd_cp = {}
    id_cp = {}
    key_compare = {}
    cbtyp_cp = {}
    cb_cp = {}

    # Process CP file
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cp_{prefix}.csv", encoding="utf-8") as cp, \
         open(f"cp_out_{prefix}.csv", "w", encoding="utf-8") as out:

        ##CP Fields 
        ##record CP,ID_ST,ID_KV,I__ND_CP,ID_CP,I__BS_CP,ID_CO,I__MEAS_CP,OPEN,ND,MRNOM,%SUBSCRIPT,ID_DECK,REGND,REGSK,REG$ND,CBTYP,CB
        #         0,    1,    2,       3,    4,       5,    6,         7,   8, 9,   10,        11,     12,   13,   14,    15,   16,17
        
        cp_idx = get_field_namespace("CP") #map of field names to indices for CP
        for line in cp:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            fields_to_write = ["ID_CO", "ID_ST", "ID_CP", "CBTYP", "CB", "ND"]
            out.write(",".join(fds[getattr(cp_idx, field)] for field in fields_to_write) + "\n")            
            key_cp = fds[cp_idx.ID_CO] + "#" + fds[cp_idx.ND]
            nd_cp[key_cp] = fds[cp_idx.ND]
            id_cp[key_cp] = fds[cp_idx.ID_CP]
            key_compare[key_cp] = key_cp
            cbtyp_cp[key_cp] = fds[cp_idx.CBTYP]
            cb_cp[key_cp] = fds[cp_idx.CB]
    
    # Build exception list from UN/LD nodes
    # avoiding getting fields by ID because ndo changes order of fields
    with open(f"exception_list_{prefix}.csv", "w", encoding="utf-8") as excep, \
         open(f"ndonly_{prefix}.txt", encoding="utf-8") as ndo:
        for line in ndo:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            key_un_ld = fds[1] + "#" + fds[3]
            if fds[3] == nd_cp.get(key_un_ld, None):
                excep.write(f"{key_un_ld}\n")

    # XF check
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv", encoding="utf-8") as xf, \
         open(f"exception_list_{prefix}.csv", "a", encoding="utf-8") as excep:
        xf_idx = get_field_namespace("XF") #map of field names to indices for XF
        for line in xf:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            stn = fds[xf_idx.ID_ST]
            nd_xf = fds[xf_idx.ND]
            znd_xf = fds[xf_idx.ZND]
            xf_nd = fds[xf_idx.ID_ST] + "#" + fds[xf_idx.ND]
            xf_znd = fds[xf_idx.ID_ST] + "#" + fds[xf_idx.ZND]
            if nd_xf == nd_cp.get(xf_nd, None):
                excep.write(f"{xf_nd}\n")
            elif znd_xf == nd_cp.get(xf_znd, None):
                excep.write(f"{xf_znd}\n")

    # LN check
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv", encoding="utf-8") as ln, \
         open(f"exception_list_{prefix}.csv", "a", encoding="utf-8") as excep:
        ln_idx = get_field_namespace("LN")
        for line in ln:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            stn = fds[ln_idx.ST_LN]
            nd_ln = fds[ln_idx.ND_LN]
            zstn = fds[ln_idx.ZST_LN]
            znd_ln = fds[ln_idx.ZND_LN]
            ln_nd = fds[ln_idx.ST_LN] + "#" + fds[ln_idx.ND_LN]
            ln_znd = fds[ln_idx.ZST_LN] + "#" + fds[ln_idx.ZND_LN]
            if nd_ln == nd_cp.get(ln_nd, None):
                excep.write(f"{ln_nd}\n")
            elif znd_ln == nd_cp.get(ln_znd, None):
                excep.write(f"{ln_znd}\n")

    # CB check for nodes with more than one CB
    key_compare2 = {}
    key_compare3 = {}
    cbtyp = {}
    id_cb = {}
    id2_cb = {}

    with open(f"cb_two_{prefix}.txt", "w", encoding="utf-8") as cb_two, \
         open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cb_{prefix}.csv", encoding="utf-8") as cb:
        cb_idx = get_field_namespace("CB")
        for line in cb:
            line = line.strip().replace("'", "")
            fds = line.split(",")
            stn = fds[cb_idx.ID_ST]
            nd_cb = fds[cb_idx.ND]
            znd_cb = fds[cb_idx.ZND]
            cb_nd = fds[cb_idx.ID_ST] + "#" + fds[cb_idx.ND]
            key_compare2[cb_nd] = cb_nd
            cb_znd = fds[cb_idx.ID_ST] + "#" + fds[cb_idx.ZND]
            key_compare3[cb_znd] = cb_znd
            st_cb_key = fds[cb_idx.ID_ST] + "#" + fds[cb_idx.ID]
            cbtyp[st_cb_key] = fds[cb_idx.ID_CBTYP]
            id_cb[cb_nd] = fds[cb_idx.ID]
            id2_cb[cb_znd] = fds[cb_idx.ID]
            if nd_cb == nd_cp.get(cb_nd, None):
                cb_two.write(f"{cb_nd}\n")
            elif znd_cb == nd_cp.get(cb_znd, None):
                cb_two.write(f"{cb_znd}\n")

    # Use system sort/uniq to create exception and final lists
    os.system(f"cat cb_two_{prefix}.txt | sort | uniq -d >> exception_list_{prefix}.csv")
    os.system(f"cat cb_two_{prefix}.txt | sort | uniq -u > final_list_{prefix}.txt")
    os.system(f"cat exception_list_{prefix}.csv | sort | uniq > exclude_list_{prefix}.txt")

    # Clean up intermediate files
    # for fname in [
    #     f"cp_out_{prefix}.csv",
    #     f"exclude_list_{prefix}.txt",
    #     f"exception_list_{prefix}.csv",
    #     f"cb_two_{prefix}.txt",
    #     f"ndonly_{prefix}.txt"
    # ]:
    #     try:
    #         os.remove(fname)
    #     except Exception:
    #         pass

    # Write RIO file
    # avoiding getting fields by ID because ndo changes order of fields

    with open(f"cp_cb_{prefix}.rio", "w", encoding="utf-8") as rio:
        rio.write("echo -c ON;\n")
        rio.write("/open_cp(*)=FALSE;\n")
        with open(f"final_list_{prefix}.txt", encoding="utf-8") as flst:
            for line in flst:
                line = line.strip().replace("'", "")
                fds = line.split("#")
                key_cpcb = fds[0] + "#" + fds[1]
                st = fds[0]
                nd = fds[1]
                if (key_cpcb == key_compare.get(key_cpcb, "") and
                    key_cpcb == key_compare2.get(key_cpcb, "") and
                    cbtyp_cp.get(key_cpcb, "") == " "):
                    cbt = cbtyp.get(st + "#" + id_cb.get(key_cpcb, ""), "")
                    _rio_ = f'find st="{fds[0]}",CP = "{id_cp.get(key_cpcb, "")}";/CB = "{id_cb.get(key_cpcb, "")}";/CBTYP = "{cbt}";'
                    rio.write(f"{_rio_}\n")
                elif (key_cpcb == key_compare.get(key_cpcb, "") and
                      key_cpcb == key_compare3.get(key_cpcb, "") and
                      cbtyp_cp.get(key_cpcb, "") == " "):
                    cbt = cbtyp.get(st + "#" + id2_cb.get(key_cpcb, ""), "")
                    _rio_ = f'find st="{fds[0]}",CP = "{id_cp.get(key_cpcb, "")}";/CB = "{id2_cb.get(key_cpcb, "")}";/CBTYP = "{cbt}";'
                    rio.write(f"{_rio_}\n")

if __name__ == "__main__":
    main()