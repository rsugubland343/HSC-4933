###########################################
#        Lab 5: Dataset Conversion        #
# ----------------------------------------#
# Remington Bland # HSC4933.005 # 10/6/26 #
###########################################

# Imports
import sys
from pathlib import Path
import pandas as pd
# import numpy as np

# Reads the CSV path the user typed after the script name
csv_path = Path(sys.argv[1])

# Checks for duplicate columns
columns = pd.read_csv(csv_path, nrows=0).columns.tolist()
duplicates = []
for column in columns:
    # Checking to see if pandas renamed a column with a number like "name.1"
    if "." in column:
        # Divides into column name and numeric suffix
        column_name = column.rsplit(".", 1)[0] # "name.1" becomes "name"
        dupe_column_number = column.rsplit(".", 1)[1] # "name.1" becomes "1"
        # If the suffix is a digit, there is a duplicate
        if dupe_column_number.isdigit() and column_name not in duplicates:
            duplicates.append(column_name)

# Exit the script if duplicate is found
if duplicates:
    sys.exit(f"Duplicate columns found. Exiting script.")

# Read the file, and convert into designated file format
df = pd.read_csv(csv_path)
out_path = f"{csv_path.stem}.parquet"
df.to_parquet(out_path, index=False)

# Tells user of the output file location
print(f"File written to {out_path}")