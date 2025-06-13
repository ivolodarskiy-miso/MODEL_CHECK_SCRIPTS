import os
import sys
from collections import defaultdict

def main():
    # Exporting LN and ZBR data (as in Perl)
    print("Exporting LN data ...")
    os.system("hdbexport -d netmom -record LN -noprependpattern -pattern data_netmom_patterns.dat >ln.txt")
    print("Exporting ZBR data ...")
    os.system("hdbexport -d netmom -record ZBR -noprependpattern -pattern data_netmom_patterns.dat >zbr.txt")

    # Count branch names
    line = defaultdict(int)

    # Process ln.txt
    with open("ln.txt", encoding="utf-8") as br:
        for l in br:
            fields = l.strip().split(",")
            key = fields[5] + "|" + fields[6]
            line[key] += 1

    # Process zbr.txt
    with open("zbr.txt", encoding="utf-8") as br:
        for l in br:
            fields = l.strip().split(",")
            key = fields[5] + "|" + fields[6]
            line[key] += 1

    # Write duplicates to file and print
    with open(f"DUPLICATE_LINE_CHECK_{sys.argv[1]}.txt", "w", encoding="utf-8") as errorout:
        for key, count in line.items():
            if count >= 2:
                print(f"Duplicate branch name {key}, {count}")
                errorout.write(f"Duplicate branch name {key}, {count}\n")

    # Remove temp files
    os.remove("ln.txt")
    os.remove("zbr.txt")

    # Write hash to CSV
    with open("hash.csv", "w", encoding="utf-8") as out:
        for key, value in line.items():
            out.write(f"{key} => {value}\n")

if __name__ == "__main__":
    main()