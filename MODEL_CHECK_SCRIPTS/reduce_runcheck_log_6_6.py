import csv
import argparse
import os

def load_exclusion_list(file_path):
    """
    Load exclusions from a CSV file. Assumes first column contains the errors to exclude.
    """
    exclusions = []
    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header row
        for row in reader:
            if row and row[0].strip():
                exclusions.append(row[0].strip())
    return exclusions

def process_log_file(log_file_path, exclusions, output_file_path):
    """
    Read the log file and write lines to the output file
    if they do not contain any of the exclusion errors.
    """
    with open(log_file_path, 'r') as log_file, open(output_file_path, 'w') as output_file:
        for line in log_file:
            if not any(exclusion in line for exclusion in exclusions):
                output_file.write(line)

def main():
    parser = argparse.ArgumentParser(description='Simplify a log file by excluding specific errors.')
    parser.add_argument('--log_file', help='Path to the log file to process')
    args = parser.parse_args()

    exclusion_file = 'log_exclusion_list.csv'
    log_file = args.log_file

    # Determine output file name
    base, ext = os.path.splitext(log_file)
    output_file = f"{base}_simplified{ext}"

    exclusions = load_exclusion_list(exclusion_file)
    process_log_file(log_file, exclusions, output_file)
    print("Simplified log file created as '{}'.".format(output_file))

if __name__ == '__main__':
    main()
