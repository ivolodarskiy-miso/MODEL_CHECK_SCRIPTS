import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: monelm_exc_check.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    tapty = {}
    sked = {}
    tab = {}

    # Process xf file
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv", encoding="utf-8") as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) > 19:
                    tapty[fields[16]] = 1
                    tapty[fields[17]] = 1
                    sked[fields[19]] = "XF|" + fields[1] + "|" + fields[2]
    except Exception:
        print("\n\n\n*****ABORT*****Could not read from xf_%s.csv\n\n\n" % prefix)
        sys.exit(1)

    # Process cp file
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cp_{prefix}.csv", encoding="utf-8") as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) > 14:
                    sked[fields[14]] = "CP|" + fields[1] + "|" + fields[4]
    except Exception:
        print("\n\n\n*****ABORT*****Could not read from cp_%s.csv\n\n\n" % prefix)
        sys.exit(1)

    # Process un file
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/un_{prefix}.csv", encoding="utf-8") as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) > 23:
                    sked[fields[23]] = "UN|" + fields[1] + "|" + fields[4]
                if len(fields) > 13:
                    tab[fields[13]] = 1
    except Exception:
        print("\n\n\n*****ABORT*****Could not read from un_%s.csv\n\n\n" % prefix)
        sys.exit(1)

    # Process sked file and write suspicious values
    try:
        susp_path = f"suspicious_regsked_{prefix}.txt"
        with open(susp_path, "w", encoding="utf-8") as susp:
            with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/sked_{prefix}.csv", encoding="utf-8") as f:
                for line in f:
                    fields = line.strip().split(',')
                    if len(fields) > 9 and fields[4] in sked:
                        try:
                            val = float(fields[9])
                            if val > 1.5 or val < 0.5:
                                susp.write(f"sked {fields[4]} for {sked[fields[4]]} suspicious! val = {fields[9]} \n")
                        except Exception:
                            continue
    except Exception:
        print("\n\n\n*****ABORT*****Could not read from sked.csv\n\n\n")
        sys.exit(1)

    # Print the suspicious file contents (like `cat`)
    os.system(f"type suspicious_regsked_{prefix}.txt")

if __name__ == "__main__":
    main()