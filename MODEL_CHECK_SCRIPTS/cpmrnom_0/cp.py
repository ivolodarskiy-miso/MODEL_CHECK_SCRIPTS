import sys
import os

def main():
    if len(sys.argv) != 2:
        print("\nUsage: cp.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    cpmrnom_file = f"cpmrnom_is_zero_{prefix}.csv"
    rio_cpmrnom_file = f"rio_cpmrnom_{prefix}.rio"
    cp_file = f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/cp_{prefix}.csv"

    try:
        cpmrnom = open(cpmrnom_file, "w", encoding="utf-8")
        rio_cpmrnom = open(rio_cpmrnom_file, "w", encoding="utf-8")
        with open(cp_file, encoding="utf-8") as cp:
            for line in cp:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                if len(fds) > 10 and fds[10] == "0":
                    cpmrnom.write(f"{fds[6]},{fds[1]},{fds[4]},{fds[2]},{fds[9]},{fds[8]},{fds[10]}\n")
                    _rio = f'find st="{fds[1]}",CP = "{fds[4]}";/mrnom = 0.01;'
                    rio_cpmrnom.write(f" {_rio}\n")
    except Exception:
        print(f"\n\n\n*****ABORT***** Could not process files for prefix {prefix}\n\n\n")
        sys.exit(1)
    finally:
        try:
            cpmrnom.close()
            rio_cpmrnom.close()
        except Exception:
            pass

    # Remove the CSV file as in the Perl script
    try:
        os.remove(cpmrnom_file)
    except Exception:
        pass

    print(f"  If you are an integrator please check this file during integration ... cleanup_rio/rio_cpmrnom_{prefix}.rio ")

if __name__ == "__main__":
    main()