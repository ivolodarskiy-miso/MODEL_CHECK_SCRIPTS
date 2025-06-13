import sys

def main():
    if len(sys.argv) != 2:
        for arg in sys.argv:
            print(arg, end=" ") 
        print("\nUsage: monelm_exc_check.py dumped_file_prefix")
        sys.exit(1)

    prefix = sys.argv[1]

    # Build sets of valid keys from Netmom files
    lines_in_netmom = set()
    xfmrs_in_netmom = set()
    zbrs_in_netmom = set()

    # LN
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/ln_{prefix}.csv", encoding="utf-8") as f:
            next(f, None)  # skip header
            for line in f:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                key = f'"{fds[2]}","{fds[3]}"'
                lines_in_netmom.add(key)
    except Exception:
        print(f"*****ABORT***** Could not read from ln_{prefix}.csv\n")
        sys.exit(1)

    # XF
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/xf_{prefix}.csv", encoding="utf-8") as f:
            next(f, None)
            for line in f:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                key = f'"{fds[1]}","{fds[2]}"'
                xfmrs_in_netmom.add(key)
    except Exception:
        print(f"*****ABORT***** Could not read from xf_{prefix}.csv\n")
        sys.exit(1)

    # ZBR
    try:
        with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/zbr_{prefix}.csv", encoding="utf-8") as f:
            next(f, None)
            for line in f:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                key = f'"{fds[1]}","{fds[2]}"'
                zbrs_in_netmom.add(key)
    except Exception:
        print(f"*****ABORT***** Could not read from zbr_{prefix}.csv\n")
        sys.exit(1)

    # Check add_monitor.csv
    try:
        with open("add_monitor.csv", encoding="utf-8") as f, \
             open(f"invalid_elements_{prefix}.csv", "w", encoding="utf-8") as errorf:
            next(f, None)
            print("Checking the add monitor Exception list")
            errorf.write("Checking the add monitor Exception list\n")
            for line in f:
                line = line.strip().replace(" ", "")
                fds = line.split(",")
                if fds[0] == "LN":
                    k = f'"{fds[1]}","{fds[2]}"'
                    if k not in lines_in_netmom:
                        msg = f"ERROR add monitor -- {k} -- {line} is no longer valid with the current Netmom \n"
                        print(msg, end="")
                        errorf.write(msg)
                elif fds[0] == "XF":
                    k = f'"{fds[1]}","{fds[2]}"'
                    if k not in xfmrs_in_netmom:
                        msg = f"ERROR add monitor -- {k} -- {line} is no longer valid with the current Netmom \n"
                        print(msg, end="")
                        errorf.write(msg)
                elif fds[0] == "ZBR":
                    k = f'"{fds[1]}","{fds[2]}"'
                    if k not in zbrs_in_netmom:
                        msg = f"ERROR add monitor -- {k} -- {line} is no longer valid with the current Netmom \n"
                        print(msg, end="")
                        errorf.write(msg)
                elif fds[0] not in ("XF", "LN", "ZBR"):
                    print(f"WARNING FLST-- {line}")
    except Exception:
        print("*****ABORT***** Could not read from add_monitor.csv\n")
        sys.exit(1)

    print("Checking the do_not_monitor Exception list")

    # Check Exception_list_do_not_monitor.csv
    try:
        with open("Exception_list_do_not_monitor.csv", encoding="utf-8") as dis_mon, \
             open(f"invalid_elements_{prefix}.csv", "a", encoding="utf-8") as errorf:
            for line in dis_mon:
                line = line.strip().replace("'", "")
                fds = line.split(",")
                if len(fds) < 10:
                    continue
                if fds[9] == "YES" and fds[0] == "LN":
                    key = f'"{fds[1]}","{fds[2]}"'
                    if key not in lines_in_netmom:
                        msg = f"ERROR Exception_do_not_monitor -- {key} -- {line} is no longer valid with the current Netmom \n"
                        print(msg, end="")
                        errorf.write(msg)
                elif fds[9] == "YES" and fds[0] == "ZBR":
                    key = f'"{fds[1]}","{fds[2]}"'
                    if key not in zbrs_in_netmom:
                        msg = f"ERROR Exception_do_not_monitor -- {key} -- {line} is no longer valid with the current Netmom \n"
                        print(msg, end="")
                        errorf.write(msg)
                elif fds[9] == "YES" and fds[0] == "XF":
                    key = f'"{fds[4]}","{fds[2]}"'
                    if key not in xfmrs_in_netmom:
                        msg = f"ERROR Exception_do_not_monitor -- {key} -- {line} is no longer valid with the current Netmom \n"
                        print(msg, end="")
                        errorf.write(msg)
    except Exception:
        print("*****ABORT Could not read from file Exception_list_do_not_monitor\n\n\n")
        sys.exit(1)

if __name__ == "__main__":
    main()