import csv
import sys
INVALID_LMT_LOWER_THRESHOLD = 0

''' This script checks exported ZBLIM, XFLIM and LNLIM files to make sure that devices don't have duplicate limits 
    tied to the same device and that all limits are valid entries'''

def check_device_column_uniqueness(input_file,):
    seen_values = set()
    duplicate_rows = []

    with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        row_number = 0 
        for row in reader:
            LMT_ID = str(row[0]+":"+row[1])
            row_number += 1
            parent_device = str(row[2]+"_"+row[3] + "_"+ row[4]).replace("'","")
            try:
                limit1, limit2, limit3 = map(float, row[-3:])
                if not all(isinstance(x, float) for x in [limit1, limit2, limit3]):
                    print(f"ERROR: {LMT_ID} has at least one invalid Limit value: {limit1},{limit2},{limit3}")
                elif (limit1 < INVALID_LMT_LOWER_THRESHOLD 
                    or limit2 < INVALID_LMT_LOWER_THRESHOLD 
                    or limit3 < INVALID_LMT_LOWER_THRESHOLD): 
                    print(f"ERROR: {LMT_ID} has at least one invalid Limit value: {limit1},{limit2},{limit3}")
                if parent_device in seen_values:
                    duplicate_rows.append(row)
                else:
                    seen_values.add(parent_device)
            except ValueError or TypeError:
                print(f"ERROR: {parent_device} has invalid limits:{limit1},{limit2},{limit3}")
    if duplicate_rows:
        for dup_row in duplicate_rows:
            dup_parent = str(dup_row[2]+"_"+dup_row[3] + "_"+ dup_row[4]).replace("'","")
            print(f"ERROR: {dup_row[0].replace('LIM','')} : {dup_parent} has duplicate limits")
    else:
        print(f"INFO: No duplicate LMTs found in {input_file})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_unique_device.py your_file.csv")
    else:
        for arg in sys.argv[1:]:
            check_device_column_uniqueness(arg)
