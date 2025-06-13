import sys
import csv
import os 

def main(prefix):
    filename = f'/modeling/MODEL_SCRIPTS/MODEL_CHECK_SCRIPTS/data_pattern/un_{prefix}.csv'
    unit_data = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                unit_data.append({
                    'co': row[6],
                    'st': row[1],
                    'id': row[4],
                    'nd': row[11],
                    'wmx': float(row[14]),
                    'wmn': float(row[15]),
                    'rmx': float(row[16]),
                    'rmn': float(row[17]),
                    'mvarate': float(row[18]),
                    'genid': row[27]}
                    )
                #

        for data in unit_data:
            # Check for suspect rmx and rmn values. Commented out to preserve original perl script logic for reference
            # if (data['rmx'] == 0 and data['rmn'] == 0) or (data['rmx'] == data['rmn']):
            #     print(f"{data['co']},{data['st']},{data['id']} ====> has suspect rmx rmn values {data['rmx']} {data['rmn']}")

            # For units if all qmin, qmax, pmin and pmax are equal to zero
            if (data['rmx'] == 0 and data['rmn'] == 0 and data['wmx'] == 0 and data['wmn'] == 0):
                print(f"{data['co']},{data['st']},{data['id']},{data['rmx']},{data['rmn']},{data['wmx']},{data['wmn']} ====> has suspect rmx rmn wmx wmn values {data['rmx']} {data['rmn']} {data['wmx']} {data['wmn']}")

            # Check if mvarate is zero or less than wmx and rmx
            if (data['mvarate'] == 0 or 
                (data['mvarate'] < abs(data['wmx']) and data['mvarate'] < abs(data['rmx']))):
                print(f"{data['co']},{data['st']},{data['id']},{data['mvarate']} ====> has suspect mvarate value {data['mvarate']}")

            # Check if un_id is not equal to genid
            if data['genid'] != data['id']:
                print(f"{data['co']},{data['st']},{data['id']},{data['genid']} ====> unit id and genid have different names {data['id']} {data['genid']}")

        print("\nFor units if mvarate is less than either wmx, wmn, rmx or rmn")
        print("Please adjust mvarate, wmx, wmn, rmx or rmn as appropriate\n")
        print("//CO,ST,ID,mvarate,wxm,wmn,rmx,rmn\n")

        # Second pass for additional checks
        for data in unit_data:
            mvamax = data['wmx']
            if 0 - data['wmn'] > mvamax:
                mvamax = 0 - data['wmn']
            if data['rmx'] > mvamax:
                mvamax = data['rmx']
            if 0 - data['rmn'] > mvamax:
                mvamax = 0 - data['rmn']
            if data['mvarate'] < mvamax:
                print(f"// {data['co']},{data['st']},{data['id']},{data['mvarate']},{data['wmx']}, {data['wmn']}, {data['rmx']}, {data['rmn']}\n")
                print(f"find st=\"{data['st']}\", un=\"{data['id']}\"; /mvarate={mvamax};")

    except FileNotFoundError:
        print(f"Couldn't read from UN_{prefix} file. Please check the file path and ensure it exists.")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage: unit_ratings_setting.py dumped_file_prefix\n")
        sys.exit()

    prefix = sys.argv[1]
    main(prefix)