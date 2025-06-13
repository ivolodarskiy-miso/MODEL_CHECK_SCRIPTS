import sys
import os
sys.path.append(r'/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/runcheck_utils')
from run_checks_util import get_field_namespace

def unique(seq):
    seen = set()
    result = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result

def main():
    if len(sys.argv) != 2:
        print("\nUsage: multiple_line_record_with_same_name.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]
    yy = 0  # hardcoded as in Perl

    # Read ND file
    id_nd = []
    st_nd = []
    kv_nd = []
    co_nd = []
    bs_nd = []
    primebs_nd = []
    cb2_nd = []
    xf2_nd = []
    ln2_nd = []
    zbr2_nd = []
    sft_nd = []
    ND_BS = []
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/nd_{prefix}.csv", encoding="utf-8") as f:
            nd_idx = get_field_namespace("ND") #map of field names to indices for ND
            for line in f:
                fields = line.strip().replace("'", "").split(",")
                id_nd.append(fields[nd_idx.ID_ND])
                st_nd.append(fields[nd_idx.ID_ST])
                kv_nd.append(fields[nd_idx.ID_KV])
                co_nd.append(fields[nd_idx.ID_CO])
                bs_nd.append(fields[nd_idx.I__BS_ND])
                primebs_nd.append(fields[nd_idx.PRIME__BS_ND])
                cb2_nd.append(fields[nd_idx.P__CB2])
                xf2_nd.append(fields[nd_idx.P__XF2])
                ln2_nd.append(fields[nd_idx.P__LN2])
                zbr2_nd.append(fields[nd_idx.P__ZBR2])
                sft_nd.append(fields[nd_idx.SFT])
                ND_BS.append(fields[nd_idx.I__BS_ND])
    except Exception as e:
        print(e)
        print("\n\n\n*****ABORT*****Could not read from nd_%s.csv\n\n\n" % prefix)
        sys.exit(1)

    # Read ZBR file
    id_zbr = []
    line_zbr = []
    num_ln_line = {}
    izbr2_zbr = []
    zzbr2_zbr = []
    ind_zbr = []
    znd_zbr = []
    st_zbr = []
    zst_zbr = []
    zbrlist = {}
    zbrdict = {}
    busarray = []
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv", encoding="utf-8") as f:
            zbr_idx = get_field_namespace("ZBR") #map of field names to indices for ZBR
            for idx, line in enumerate(f):
                fields = line.strip().replace("'", "").split(",")
                id_zbr.append(fields[zbr_idx.ID_ZBR])
                line_zbr.append(fields[zbr_idx.ID_LINE])
                num_ln_line[fields[zbr_idx.ID_LINE]] = num_ln_line.get(fields[zbr_idx.ID_LINE], 0) + 1
                izbr2_zbr.append(fields[zbr_idx.I__ZBR2_ZBR])
                zzbr2_zbr.append(fields[zbr_idx.Z__ZBR2_ZBR])
                ind_zbr.append(int(fields[zbr_idx.I__ND_ZBR]))
                znd_zbr.append(int(fields[zbr_idx.Z__ND_ZBR]))
                st_zbr.append(fields[zbr_idx.ST_ZBR])
                zst_zbr.append(fields[zbr_idx.ZST_ZBR])
                zbr_key = fields[zbr_idx.ID_LINE] + '$' + fields[zbr_idx.ID_ZBR]
                zbrlist[zbr_key] = [ND_BS[ind_zbr[idx]-1], ND_BS[znd_zbr[idx]-1]]
                zbr_key = fields[zbr_idx.ID_LINE] + '$' + fields[zbr_idx.ID_ZBR]
                zbrdict[zbr_key] = [fields[zbr_idx.ST_ZBR], fields[zbr_idx.ZST_ZBR], ND_BS[ind_zbr[idx]-1], ND_BS[znd_zbr[idx]-1]]
                busarray.append(ND_BS[ind_zbr[idx]-1])
                busarray.append(ND_BS[znd_zbr[idx]-1])
    except Exception as e:
        print(e)
        print("\n\n\n*****ABORT*****Could not read from zbr_%s.csv\n\n\n" % prefix)
        sys.exit(1)

    # Write ZBRlist
    with open(f"ZBRlist_{prefix}", "w", encoding="utf-8") as zbrlistf:
        if yy == 1: # should never occur as YY is hardcoded
            for k, v in zbrlist.items():
                zbrlistf.write(f"{k},{v[0]},{v[1]}\n")
        else:
            for k, v in zbrlist.items():
                if v[0] != v[1]:
                    zbrlistf.write(f"{k},{v[0]},{v[1]}\n")

    # Unique bus numbers
    out = sorted(busarray)
    unique_BS = unique(out)
    with open(f"BSlist_{prefix}", "w", encoding="utf-8") as bslistf:
        for bs in unique_BS:
            bslistf.write(f"{bs}\n")

    # Build bs_hash from ZBRlist
    bs_hash = {}
    with open(f"ZBRlist_{prefix}", encoding="utf-8") as zbrlistf:
        for line in zbrlistf:
            fields = line.strip().replace("'", "").split(",")
            for idx in [1, 2]:
                if fields[idx] not in bs_hash:
                    bs_hash[fields[idx]] = fields[0]
                else:
                    bs_hash[fields[idx]] += "," + fields[0]

    # Write BS_hash
    with open(f"BS_hash_{prefix}", "w", encoding="utf-8") as bshashf:
        for k, v in bs_hash.items():
            tempv = v.split(",")
            tempvv = unique(tempv)
            tempvvv = ",".join(tempvv)
            bs_hash[k] = tempvvv
            bshashf.write(f"{k},{tempvvv}\n")

    # Build bs_hash_array
    bs_hash_array = {}
    for k, v in bs_hash.items():
        bs_hash_array[k] = v.split(",")

    print("\nsearching for zbrloops...\n")

    # Find islands
    island_bs = {}
    island_zbr = {}
    size = len(unique_BS)
    island_index = 1
    for count in range(size):
        bs = unique_BS[count]
        if bs in bs_hash_array:
            tempzbr = bs_hash_array[bs]
            tempbs = [bs]
            isect_index = 1
            while isect_index:
                isect_index = 0
                for k in list(bs_hash_array.keys()):
                    ndreference = bs_hash_array[k]
                    # intersection
                    if island_zbr.get(island_index):
                        tempzbr = list(island_zbr[island_index])
                    union = set(tempzbr)
                    isect = set()
                    for e in ndreference:
                        if e in union:
                            isect.add(e)
                    if isect:
                        tempbs += [k]
                        unique_bsmerge = unique(tempbs)
                        island_bs[island_index] = unique_bsmerge
                        tempzbr += ndreference
                        unique_zbrmerge = unique(tempzbr)
                        island_zbr[island_index] = unique_zbrmerge
                        del bs_hash_array[k]
                        isect_index += 1
            island_index += 1
            if bs in bs_hash_array:
                del bs_hash_array[bs]

    # Unique bus numbers for islands
    # Read exceptions
    exception = set()
    try:
        with open("zbrloop_exceptions.csv", encoding="utf-8") as exceptions:
            for line in exceptions:
                exception.add(line.strip())
    except Exception:
        pass

    # Write zbr log
    with open(f"zbr_{prefix}.log", "w", encoding="utf-8") as zbrlog:
        zbrloop_index = 1
        for k in sorted(island_zbr.keys()):
            tempzbrgroup = island_zbr[k]
            sizezbr = len(tempzbrgroup) + 1
            tempbsgroup = island_bs[k]
            sizebs = len(tempbsgroup)
            if sizebs < sizezbr:
                if tempbsgroup[0] != "1":  # dead bus does not count
                    tempzbrstr = ",".join(tempzbrgroup)
                    tempbsstr = ",".join(tempbsgroup)
                    if tempzbrstr in exception:
                        continue
                    zbrlog.write(f"zbrloop {zbrloop_index}==>{tempzbrstr}.....bus number:{tempbsstr}\n")
                    for zbrkey in tempzbrgroup:
                        if zbrkey in zbrdict:
                            zbrlog.write(f"    ST: {zbrdict[zbrkey][0]}, ZST: {zbrdict[zbrkey][1]},....FromBS:{zbrdict[zbrkey][2]},ToBS:{zbrdict[zbrkey][3]}\n")
                    zbrloop_index += 1

    print("\n")
    if zbrloop_index == 1:
        print("************congratulations! no zbr-loop found!************\n\n\n")
    else:
        print(f"************check zbr_{prefix}.log for more details************\n\n\n")

    # Cleanup
    for fname in [f"BSlist_{prefix}", f"ZBRlist_{prefix}", f"BS_hash_{prefix}"]:
        try:
            os.remove(fname)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    main()