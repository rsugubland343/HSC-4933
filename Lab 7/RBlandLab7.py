############################################
#         Lab 7: Linear Regression         #
# -----------------------------------------#
# Remington Bland # HSC4933.005 # 10/10/26 #
############################################

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pathlib import Path
import sys

# Prompts the user to enter a file name
# Loop used for verifying file
while True:
    filename = input("Enter the file name (or press Enter to quit): ").strip()
    # Closes the program if file is not found
    if not filename:
        print("No file name provided")
        sys.exit()

    path = Path(filename)
    # Checks to see if file exists
    if path.is_file():
        # File exists
        print("File [" + filename + "] exists.")
        break
    else:
        # Loop repeats and prompts the user again
        print("File [" + filename + "] was not found.")
        print()

# Load the dataset
df = pd.read_csv(filename)
# Loads uncleaned columns
print()
print("--- Original column names ---")
print(list(df.columns))
# Displays original data types
print(df.dtypes)

# Helps change column names to snake case
# Converts columns to all-lowercase and replaces spaces with underscores
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Cleaned column names
print()
print("--- Cleaned column names to (snakecase) ---")
print(list(df.columns))

# Asks for the x column
while True:
    x_col = input("Choose the X column: ").strip()

    # No columns were entered
    if not x_col:
        print("No column entered.")
        sys.exit()

    # If column name does not exist
    if x_col not in df.columns:
        print("Error: '" + x_col + "' is not a valid column name. Try again.")
    else:
        break

# Asks for the y column
while True:
    y_col = input("Choose the y column: ").strip()

    # No columns were entered
    if not y_col:
        print("No column entered.")
        sys.exit()

    # If column name does not exist
    if (y_col not in df.columns):
        print("Error: '" + y_col + "' is not a valid column name. Try again.")
    elif (y_col == x_col):
        print("Error '" + x_col
              + "' is already taken. Pick a different column.")
    else:
        break

# Checks if data in x column is numeric, removing commas if necessary
print(df[x_col].dtype)
is_numeric = pd.api.types.is_numeric_dtype(df[x_col])
if is_numeric:
    print("x_col is numeric")
else:
    # Removes commas
    df[x_col] = df[x_col].str.replace(",", "")
    # Converts data to numeric
    df[x_col] = pd.to_numeric(df[x_col], errors="coerce")
print(df[x_col].dtype)

# Checks if data in y column is numeric, removing commas if necessary
print(df[y_col].dtype)
is_numeric = pd.api.types.is_numeric_dtype(df[y_col])
if is_numeric:
    print("y_col is numeric")
else:
    # Removes commas
    df[y_col] = df[y_col].str.replace(",", "")
    # Converts data to numeric
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
print(df[y_col].dtype)

# Drops any rows with missing x or y values
rows_before = len(df)
data = df.dropna(subset = [x_col, y_col])
rows_after = len(data)
skipped = rows_before - rows_after
print("Skipped: " + str(skipped))

# Prompts user for scatterplot without the regression line output filename
while True:
    output_filename = input("Enter the file name (or press Enter to quit): ").strip()
    # Closes the program if file is not found
    if not output_filename:
        print("No file name provided")
        sys.exit()
    else:
        break

# Creates a scatter plot without the regression line
fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(data[x_col], data[y_col], alpha=0.6, edgecolors="k", linewidth=0.3)
ax.set_xlabel(x_col)
ax.set_ylabel(y_col)
ax.set_title(f"{y_col} vs {x_col} (n = {len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()

# Saves the scatterplot
fig.savefig(output_filename, dpi=300)

# Print save was successful
print(f"Saved scatterplot -> {output_filename}")

# Prompts user for scatterplot with the regression line output filename
while True:
    output_filename = input("Enter the OLS file name (or press Enter to quit): ").strip()
    # Closes the program if file is not found
    if not output_filename:
        print("No file name provided")
        sys.exit()
    else:
        break

# Perform linear regression
X = sm.add_constant(data[x_col])
model = sm.OLS(data[y_col], X).fit()

# Print the regression summary
print("OLS Regression Summary: ")
print(model.summary())

# Make a new scatter plot with regression line
x_line = np.linspace(data[x_col].min(), data[x_col].max(), 100)
y_line = model.params["const"] + model.params[x_col] * x_line
ax.plot(x_line, y_line, color="crimson", linewidth=2, label=f"OLS line (R² = {model.rsquared:.3f})")
ax.set_title(f"{y_col} vs {x_col} with OLS line (n = {len(data)})")
ax.legend()

# Save new scatterplot
fig.savefig(output_filename, dpi=300)

# Print save was successful
print(f"Saved scatterplot with OLS line -> {output_filename}")

# Display OLS regression figure in the pop-up menu
plt.show()
