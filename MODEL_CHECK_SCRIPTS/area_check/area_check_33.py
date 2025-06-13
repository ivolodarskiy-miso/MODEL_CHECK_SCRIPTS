import sys

# ------------------------------------------------------------------------------------------
# Cross-check area records in netmom and ../AREA_UPDATE/area_flags_RTO.csv
# When there is an area change, it is expected to update the flag file accordingly
# ------------------------------------------------------------------------------------------

# Check arguments
if len(sys.argv) != 2:
    print("\nUsage: area_check_33.py dumped_file_prefix\n")
    sys.exit(1)

prefix = sys.argv[1]

# -----------------------------------------------------------------------------------------------
# Read AREA file
id_area = []
iso_area = []
loss_area = []
misoable_area = []
match_area = []
try:
    with open(f"/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/area_{prefix}.csv", "r") as AREA:
        

        for line in AREA:
            line = line.rstrip("\n")
            line = line.replace("'", "")
            fields = line.split(",")
            id_area.append(fields[2])
            iso_area.append(fields[3])
            loss_area.append(fields[4])
            misoable_area.append(fields[5])
            # region_area.append(fields[6])  # Uncomment if needed
            # useos_area.append(fields[7])  # Uncomment if needed
            match_area.append(0)
except FileNotFoundError:
    print("*****ABORT***** Could not read from AREA file\n\n\n")
    sys.exit(1)

# -----------------------------------------------------------------------------------------------
# Read FLAG file
try:
    with open("/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/AREA_UPDATE/area_flags_RTO.csv", "r") as FLAG:
        for line in FLAG:
            line = line.rstrip("\n")
            line = line.replace("'", "")
            fields = line.split(",")
            if fields[0] != "AREA_ID":
                area = fields[0]
                match_netmom = 0
                for j in range(len(id_area)):
                    if area == id_area[j]:
                        match_netmom = 1
                        if fields[2] != iso_area[j]:
                            print(f"ISO diff: {fields[0]}, iso={iso_area[j]} -> {line}")
                        if fields[3] != loss_area[j]:
                            print(f"LOSS diff: {fields[0]}, loss={loss_area[j]} -> {line}")
                        if fields[4] != misoable_area[j]:
                            print(f"MISOABLE diff: {fields[0]}, misoable={misoable_area[j]} -> {line}")
                        # Uncomment if needed
                        # if fields[5] != region_area[j]:
                        #     print(f"REGION diff: {fields[0]}, region={region_area[j]} -> {line}")
                        match_area[j] = 1
                if match_netmom == 0:
                    print(f"area {area} not in netmom")
except FileNotFoundError:
    print("*****ABORT***** Could not read from area_flags_RTO.csv file\n\n\n")
    sys.exit(1)

# -----------------------------------------------------------------------------------------------
# Check for unmatched areas
for j in range(len(id_area)):
    if match_area[j] == 0:
        print(f"area {id_area[j]} not in AREA_UPDATE/area_flags_RTO.csv")

