import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: avr_regnd_bulk.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]
    xf_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv"
    out_file = f"avr_regnd_{prefix}.csv"

    try:
        XF = open(xf_file, encoding="utf-8")
    except Exception:
        print(f"*****ABORT***** Could not read from xf_{prefix}.csv\n")
        sys.exit(1)

    avr_regnd = open(out_file, "w", encoding="utf-8")
    avr_regnd.write("CO, ST, XFMR, XF, ND, ZND, AVR, REGND\n")

    for line in XF:
        line = line.strip().replace("'", "")
        fields = line.split(",")
        if len(fields) > 20:
            co = fields[7]
            st = fields[1]
            xfmr = fields[8]
            xf = fields[2]
            nd = fields[12]
            znd = fields[13]
            avr = fields[20]
            regnd = fields[18]
            if (avr == "T" and (regnd == ' ' or regnd == "")):
                avr_regnd.write(f"{co},{st},XFMR -- {xfmr},XF -- {xf},ND -- {nd},ZND -- {znd},AVR -- {avr},Regnd -- {regnd}\n")

    XF.close()
    avr_regnd.close()

    # Print the output file contents (like `cat`)
    with open(out_file, encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    main()