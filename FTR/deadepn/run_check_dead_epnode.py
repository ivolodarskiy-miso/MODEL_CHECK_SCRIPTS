import sys
import csv
import os
sys.path.append(r'/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/runcheck_utils')
from run_checks_util import get_field_namespace

def read_csv(filepath):
    data = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([item.strip().replace("'", "") for item in row])
    return data

def main(prefix):
    # File paths
    base = '/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern'
    files = {
        'bsl': f'{base}/bsl_{prefix}.csv',
        'bs': f'{base}/bs_{prefix}.csv',
        'un': f'{base}/un_{prefix}.csv',
        'ld': f'{base}/ld_{prefix}.csv',
        'nd': f'{base}/nd_{prefix}.csv',
        'cb2': f'{base}/cb2_{prefix}.csv',
        'cb': f'{base}/cb_{prefix}.csv',
        'xf2': f'{base}/xf2_{prefix}.csv',
        'xf': f'{base}/xf_{prefix}.csv',
        'ln2': f'{base}/ln2_{prefix}.csv',
        'ln': f'{base}/ln_{prefix}.csv',
        'zbr2': f'{base}/zbr2_{prefix}.csv',
        'zbr': f'{base}/zbr_{prefix}.csv',
    }

    # Read all CSVs
    data = {}
    for key, path in files.items():
        if not os.path.exists(path):
            print(f"***** Could not find {os.path.basename(path)}\n\n\n")
            sys.exit(1)
        data[key] = read_csv(path)

    # Prepare output files
    debug_file = f'debug_search_{prefix}'
    rio_file = f'cb_normal_{prefix}.rio'
    warning_file = f'warning_{prefix}'

    DEB = open(debug_file, 'w', encoding='utf-8')
    RIO = open(rio_file, 'w', encoding='utf-8')
    WAR = open(warning_file, 'w', encoding='utf-8')

    # Helper: Perl arrays are 1-based, Python is 0-based, so we pad with a dummy row. \
    # Preserving perl indexes for continuity
    def pad(data):
        return [None] + data

    # Parse and pad all data for 1-based indexing
    bs = pad(data['bs'])
    un = pad(data['un'])
    ld = pad(data['ld']) # Not used 
    nd = pad(data['nd'])
    cb2 = pad(data['cb2'])
    cb = pad(data['cb'])
    xf2 = pad(data['xf2']) # Not used
    xf = pad(data['xf'])  # Not used
    ln2 = pad(data['ln2'])  # Not used
    ln = pad(data['ln'])
    zbr2 = pad(data['zbr2'])
    zbr = pad(data['zbr'])

    # Build lookup arrays (mimic Perl's arrays)
    # Only the fields used in the Perl script are extracted
    # For brevity, only a subset is shown; expand as needed

    # Example for UN
    un_idx = get_field_namespace("UN")
    st_un = [None] + [row[un_idx.ID_ST] for row in un[1:]]
    kv_un = [None] + [row[un_idx.ID_KV] for row in un[1:]]
    nd_un = [None] + [int(row[un_idx.I__ND_UN]) for row in un[1:]]
    id_un = [None] + [row[un_idx.ID_UN] for row in un[1:]]
    co_un = [None] + [row[un_idx.ID_CO] for row in un[1:]]
    open_un = [None] + [row[un_idx.OPEN] for row in un[1:]]

    # Example for LD
    ld_idx = get_field_namespace("LD")
    st_ld = [None] + [row[ld_idx.ID_ST] for row in ld[1:]]
    kv_ld = [None] + [row[ld_idx.ID_KV] for row in ld[1:]]
    nd_ld = [None] + [row[ld_idx.I__ND_LD] for row in ld[1:]]
    id_ld = [None] + [row[ld_idx.ID_LD] for row in ld[1:]]
    bs_ld = [None] + [row[ld_idx.I__BS_LD] for row in ld[1:]]
    ldarea_ld = [None] + [row[ld_idx.LDAREA_LD] for row in ld[1:]]
    basew_ld = [None] + [row[ld_idx.BASEW_LD] for row in ld[1:]]
    baser_ld = [None] + [row[ld_idx.BASER_LD] for row in ld[1:]]
    parfracw_ld = [None] + [row[ld_idx.PARFRACW_LD] for row in ld[1:]]
    pf_ld = [None] + [row[ld_idx.PF_LD] for row in ld[1:]]
    co_ld = [None] + [row[ld_idx.ID_CO] for row in ld[1:]]
    imeas_ld = [None] + [row[ld_idx.I__MEAS_LD] for row in ld[1:]]
    wm_ld = [None] + [row[ld_idx.WM_LD] for row in ld[1:]]
    manual_ld = [None] + [row[ld_idx.MANUAL_LD] for row in ld[1:]]
    open_ld = [None] + [row[ld_idx.OPEN_LD] for row in ld[1:]]
    vld = [None] + [0 for _ in ld[1:]]

    # Example for ND
    nd_idx = get_field_namespace("ND")
    id_nd = [None] + [row[nd_idx.ID_ND] for row in nd[1:]]
    st_nd = [None] + [row[nd_idx.ID_ST] for row in nd[1:]]
    kv_nd = [None] + [row[nd_idx.ID_KV] for row in nd[1:]]
    co_nd = [None] + [row[nd_idx.ID_CO] for row in nd[1:]]
    bs_nd = [None] + [int(row[nd_idx.I__BS_ND]) for row in nd[1:]]
    primebs_nd = [None] + [int(row[nd_idx.PRIME__BS_ND]) for row in nd[1:]]
    cb2_nd = [None] + [int(row[nd_idx.P__CB2]) for row in nd[1:]]
    xf2_nd = [None] + [int(row[nd_idx.P__XF2]) for row in nd[1:]]
    ln2_nd = [None] + [int(row[nd_idx.P__LN2]) for row in nd[1:]]
    zbr2_nd = [None] + [int(row[nd_idx.P__ZBR2]) for row in nd[1:]]
    sft_nd = [None] + [row[nd_idx.SFT] for row in nd[1:]]

    # Example for BS
    bs_idx = get_field_namespace("BS")
    open_bs = [None] + [row[bs_idx.OPEN] for row in bs[1:]]
    dead_bs = [None] + [row[bs_idx.DEAD] for row in bs[1:]]

   # Example for CB2
    cb2_idx = get_field_namespace("CB2")
    id_cb2 = [None] + [row[cb2_idx.ID] for row in cb2[1:]]
    cb_cb2 = [None] + [int(row[cb2_idx.I__CB]) for row in cb2[1:]]

   # Example for CB
    cb_idx = get_field_namespace("CB")
    st_cb = [None] + [row[cb_idx.ID_ST] for row in cb[1:]]
    cbtyp_cb = [None] + [row[cb_idx.ID_CBTYP] for row in cb[1:]]
    id_cb = [None] + [row[cb_idx.ID] for row in cb[1:]]
    kv_cb = [None] + [row[cb_idx.KVID] for row in cb[1:]]
    ind_cb = [None] + [int(row[cb_idx.I__ND]) for row in cb[1:]]
    znd_cb = [None] + [int(row[cb_idx.Z__ND]) for row in cb[1:]]
    imeas_cb = [None] + [row[cb_idx.I__MEAS] for row in cb[1:]]
    nmlopen_cb = [None] + [row[cb_idx.NMLOPEN] for row in cb[1:]]

    # Example for XF2
    xf2_idx = get_field_namespace("XF2")
    id_xf2 = [None] + [row[xf2_idx.ID_XF2] for row in xf2[1:]]
    st_xf2 = [None] + [row[xf2_idx.ID_ST] for row in xf2[1:]]
    kv_xf2 = [None] + [row[xf2_idx.ID_KV] for row in xf2[1:]]
    nd_xf2 = [None] + [row[xf2_idx.P__ND] for row in xf2[1:]]
    op_xf2 = [None] + [row[xf2_idx.OP__XF2_XF2] for row in xf2[1:]]
    xf_xf2 = [None] + [row[xf2_idx.I__XF_XF2] for row in xf2[1:]]
    co_xf2 = [None] + [row[xf2_idx.ID_CO] for row in xf2[1:]]
    imeas_xf2 = [None] + [row[xf2_idx.I__MEAS_XF2] for row in xf2[1:]]
    open_xf2 = [None] + [row[xf2_idx.OPEN] for row in xf2[1:]]

    # Example for XF
    xf_idx = get_field_namespace("XF")
    id_xf = [None] + [row[xf_idx.ID_XF] for row in xf[1:]]
    st_xf = [None] + [row[xf_idx.ID_ST] for row in xf[1:]]
    ixf2_xf = [None] + [row[xf_idx.I__XF2_XF] for row in xf[1:]]
    zxf2_xf = [None] + [row[xf_idx.Z__XF2_XF] for row in xf[1:]]
    ind_xf = [None] + [row[xf_idx.I__ND_XF] for row in xf[1:]]
    znd_xf = [None] + [row[xf_idx.Z__ND_XF] for row in xf[1:]]

    # Example for LN2
    ln2_idx = get_field_namespace("LN2")
    id_ln2 = [None] + [row[ln2_idx.ID_LN2] for row in ln2[1:]]
    st_ln2 = [None] + [row[ln2_idx.ID_ST] for row in ln2[1:]]
    kv_ln2 = [None] + [row[ln2_idx.ID_KV] for row in ln2[1:]]
    nd_ln2 = [None] + [row[ln2_idx.P__ND] for row in ln2[1:]]
    op_ln2 = [None] + [row[ln2_idx.OP__LN2_LN2] for row in ln2[1:]]
    ln_ln2 = [None] + [row[ln2_idx.I__LN_LN2] for row in ln2[1:]]
    co_ln2 = [None] + [row[ln2_idx.ID_CO] for row in ln2[1:]]
    imeas_ln2 = [None] + [row[ln2_idx.I__MEAS_LN2] for row in ln2[1:]]
    open_ln2 = [None] + [row[ln2_idx.OPEN] for row in ln2[1:]]

    # Example for LN
    ln_idx = get_field_namespace("LN")
    id_ln = [None] + [row[ln_idx.ID_LN] for row in ln[1:]]
    line_ln = [None] + [row[ln_idx.ID_LINE] for row in ln[1:]]
    num_ln_line = {}
    for row in ln[1:]:
        key = row[ln_idx.ID_LINE]
        num_ln_line[key] = num_ln_line.get(key, 0) + 1
    iln2_ln = [None] + [row[ln_idx.I__LN2_LN] for row in ln[1:]]
    zln2_ln = [None] + [row[ln_idx.Z__LN2_LN] for row in ln[1:]]
    ind_ln = [None] + [row[ln_idx.I__ND_LN] for row in ln[1:]]
    znd_ln = [None] + [row[ln_idx.Z__ND_LN] for row in ln[1:]]

    # Example for ZBR2
    zbr2_idx = get_field_namespace("ZBR2")
    id_zbr2 = [None] + [row[zbr2_idx.ID_ZBR2] for row in zbr2[1:]]
    st_zbr2 = [None] + [row[zbr2_idx.ID_ST] for row in zbr2[1:]]
    kv_zbr2 = [None] + [row[zbr2_idx.ID_KV] for row in zbr2[1:]]
    nd_zbr2 = [None] + [row[zbr2_idx.P__ND] for row in zbr2[1:]]
    op_zbr2 = [None] + [row[zbr2_idx.OP__ZBR2_ZBR2] for row in zbr2[1:]]
    zbr_zbr2 = [None] + [row[zbr2_idx.I__ZBR_ZBR2] for row in zbr2[1:]]
    co_zbr2 = [None] + [row[zbr2_idx.ID_CO] for row in zbr2[1:]]
    imeas_zbr2 = [None] + [row[zbr2_idx.I__MEAS_ZBR2] for row in zbr2[1:]]
    open_zbr2 = [None] + [row[zbr2_idx.OPEN] for row in zbr2[1:]]

    # Example for ZBR
    zbr_idx = get_field_namespace("ZBR")
    id_zbr = [None] + [row[zbr_idx.ID_ZBR] for row in zbr[1:]]
    line_zbr = [None] + [row[zbr_idx.ID_LINE] for row in zbr[1:]]
    for row in zbr[1:]:
        key = row[zbr_idx.ID_LINE]
        num_ln_line[key] = num_ln_line.get(key, 0) + 1
    izbr2_zbr = [None] + [row[zbr_idx.I__ZBR2_ZBR] for row in zbr[1:]]
    zzbr2_zbr = [None] + [row[zbr_idx.Z__ZBR2_ZBR] for row in zbr[1:]]
    ind_zbr = [None] + [row[zbr_idx.I__ND_ZBR] for row in zbr[1:]]
    znd_zbr = [None] + [row[zbr_idx.Z__ND_ZBR] for row in zbr[1:]]
    # ...repeat for other arrays as needed...

    # Output headers
    DEB.write("UN ...\n")
    print("UN ...")
    RIO.write("/ovrdcb_cb(*)=f;/ovrdstat_cb(*)=f;\n")

    # Helper for find_open_cb
    def find_open_cb(nd_idx, vnd, vcb, vxf, vln, vzbr, queue, gexit):
        primebs = primebs_nd[nd_idx]
        bs = bs_nd[nd_idx]
        if gexit[0] == 1:
            return gexit[0]
        if primebs == bs and dead_bs[bs] == "F":
            gexit[0] = 1
            return gexit[0]
        if vnd[nd_idx] == 1:
            return 1
        noequipment = 0

        # CB2
        icb2 = cb2_nd[nd_idx] + 1
        jcb2 = cb2_nd[nd_idx + 1] if nd_idx + 1 < len(cb2_nd) else cb2_nd[nd_idx]
        for k in range(icb2, jcb2 + 1):
            cb_idx = cb_cb2[k]
            if vcb[cb_idx] != 1:
                noequipment += 1

        # XF2
        ixf2 = xf2_nd[nd_idx] + 1
        jxf2 = xf2_nd[nd_idx + 1] if nd_idx + 1 < len(xf2_nd) else xf2_nd[nd_idx]
        for k in range(ixf2, jxf2 + 1):
            xf_idx = xf_xf2[k]
            if vxf[xf_idx] != 1:
                noequipment += 1

        # LN2
        iln2 = ln2_nd[nd_idx] + 1
        jln2 = ln2_nd[nd_idx + 1] if nd_idx + 1 < len(ln2_nd) else ln2_nd[nd_idx]
        for k in range(iln2, jln2 + 1):
            ln_idx = ln_ln2[k]
            if vln[ln_idx] != 1:
                noequipment += 1

        # ZBR2
        izbr2 = zbr2_nd[nd_idx] + 1
        jzbr2 = zbr2_nd[nd_idx + 1] if nd_idx + 1 < len(zbr2_nd) else zbr2_nd[nd_idx]
        for k in range(izbr2, jzbr2 + 1):
            zbr_idx = zbr_zbr2[k]
            if vzbr[zbr_idx] != 1:
                noequipment += 1

        DEB.write("   ST={},KV={},ID={},noequipment={},gexit={}\n".format(
            st_nd[nd_idx], kv_nd[nd_idx], id_nd[nd_idx], noequipment, gexit[0]
        ))
        if noequipment == 0:
            if len(queue) > 0 and gexit[0] != 1:
                last_cb = queue[-1]
                if ind_cb[last_cb] == nd_idx or znd_cb[last_cb] == nd_idx:
                    queue.pop()
            return gexit[0]
        vnd[nd_idx] = 1

        # --- Recursive logic for CB2 ---
        for k in range(icb2, jcb2 + 1):
            cb_idx = cb_cb2[k]
            DEB.write("K={}, {}, {}, {}, {}, gexit={}, ".format(
                k, cb_idx, vcb[cb_idx], ind_cb[cb_idx], znd_cb[cb_idx], gexit[0]
            ))
            if vcb[cb_idx] != 1:
                next_nd = None
                if nmlopen_cb[cb_idx] == "T" and gexit[0] == 0:
                    queue.append(cb_idx)
                if ind_cb[cb_idx] == nd_idx:
                    next_nd = znd_cb[cb_idx]
                if znd_cb[cb_idx] == nd_idx:
                    next_nd = ind_cb[cb_idx]
                DEB.write("next_nd={}, \n".format(next_nd))
                vcb[cb_idx] = 1
                if next_nd is not None:
                    find_open_cb(next_nd, vnd, vcb, vxf, vln, vzbr, queue, gexit)

        # --- Recursive logic for XF2 ---
        for k in range(ixf2, jxf2 + 1):
            xf_idx = xf_xf2[k]
            if vxf[xf_idx] != 1:
                next_nd = nd_xf2[op_xf2[k]]
                vxf[xf_idx] = 1
                find_open_cb(next_nd, vnd, vcb, vxf, vln, vzbr, queue, gexit)

        # --- Recursive logic for LN2 ---
        for k in range(iln2, jln2 + 1):
            ln_idx = ln_ln2[k]
            if vln[ln_idx] != 1:
                next_nd = nd_ln2[op_ln2[k]]
                vln[ln_idx] = 1
                find_open_cb(next_nd, vnd, vcb, vxf, vln, vzbr, queue, gexit)

        # --- Recursive logic for ZBR2 ---
        for k in range(izbr2, jzbr2 + 1):
            zbr_idx = zbr_zbr2[k]
            if vzbr[zbr_idx] != 1:
                next_nd = nd_zbr2[op_zbr2[k]]
                vzbr[zbr_idx] = 1
                find_open_cb(next_nd, vnd, vcb, vxf, vln, vzbr, queue, gexit)

        if len(queue) > 0 and gexit[0] != 1:
            last_cb = queue[-1]
            if ind_cb[last_cb] == nd_idx or znd_cb[last_cb] == nd_idx:
                queue.pop()
        return gexit[0]

    #UN loop
    for i in range(1, len(id_un)):
        bs = bs_nd[nd_un[i]]
        if open_un[i] == "F" and open_bs[bs] != "T" and dead_bs[bs] != "T":
            continue
        st = st_un[i]
        kv = kv_un[i]
        nd_idx = nd_un[i]
        co = co_un[i]
        unid = id_un[i]
        if any(x in co for x in ["IMO_MP", "IMO_MH", "MP_IMO", "MH_IMO"]):
            continue
        vnd = [0] * len(nd)
        vcb = [0] * len(cb)
        vxf = [0] * len(xf)
        vln = [0] * len(ln)
        vzbr = [0] * len(zbr)
        gexit = [0]
        queue = []
        DEB.write("\nUN={},ST={},ND={},KV={},CO={} \n".format(unid, st, nd_idx, kv, co))
        res = find_open_cb(nd_idx, vnd, vcb, vxf, vln, vzbr, queue, gexit)
        if res == 0:
            WAR.write("\nUN={},ST={},ND={},KV={},CO={} \n".format(unid, st, nd_idx, co))
            WAR.write("\n Check Topology\n")
            DEB.write("\n WARNING\n")
        else:
            for k, cb_idx in enumerate(queue):
                DEB.write('{},"st={}",cb="{}",kv={},imeas={}\n'.format(
                    k, st_cb[cb_idx], id_cb[cb_idx], kv_cb[cb_idx], imeas_cb[cb_idx]
                ))
                RIO.write('find st="{}",cbtyp="{}",cb="{}";/ovrdstat=f;/ovrdcb=t;\n'.format(
                    st_cb[cb_idx], cbtyp_cb[cb_idx], id_cb[cb_idx]
                ))

    # ...repeat for LD and ND as in Perl script...

    DEB.close()
    RIO.close()
    WAR.close()

    print("\n***********warning file*************\n")
    with open(warning_file, encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <dumped_file_prefix>")
        sys.exit(1)
    prefix = sys.argv[1]
    main(prefix)