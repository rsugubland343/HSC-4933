##########################################################
#     Lab 8: # Linear Regression - Peer Code Review      #
#               Remington Bland  10/18/2026              #
#--------------------------------------------------------#
#                     blandr@usf.edu                     #
#--------------------------------------------------------#

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


# 1. Prompt user for dataset and load CSV
CSV_PATH = input("Enter the CSV dataset file name: ")
df = pd.read_csv(CSV_PATH)


# 2. Clean column names to snake_case
df.columns = (df.columns.str.lower().str.replace(" ", "_"))


# 3. List available column names
print("\nAvailable columns:")
print(df.columns.tolist())


# 4. Prompt user for X and Y variables
X_COL = input("\nEnter the X variable: ").strip().lower()
Y_COL = input("Enter the Y variable: ").strip().lower()
X_MIN = input("\nEnter the X variable starting point: ").strip().lower()
X_MIN_FLT = float(X_MIN)
X_MAX = input("\nEnter the X variable ending point: ").strip().lower()
X_MAX_FLT = float(X_MAX)
Y_MIN = input("\nEnter the Y variable starting point: ").strip().lower()
Y_MIN_FLT = float(Y_MIN)
Y_MAX = input("\nEnter the Y variable ending point: ").strip().lower()
Y_MAX_FLT = float(Y_MAX)

# 5. Remove rows missing X or Y values
data = df[[X_COL, Y_COL]].copy()

# Checks if data in x column is numeric, removing commas if necessary
print(df[X_COL].dtype)
is_numeric = pd.api.types.is_numeric_dtype(data[X_COL])
if is_numeric:
    print("X_COL is numeric")
else:
    # Removes commas
    data[X_COL] = data[X_COL].str.replace(",", "")
    # Converts data to numeric
    data[X_COL] = pd.to_numeric(data[X_COL], errors="coerce")
print(data[X_COL].dtype)

# Checks if data in y column is numeric, removing commas if necessary
print(data[Y_COL].dtype)
is_numeric = pd.api.types.is_numeric_dtype(data[Y_COL])
if is_numeric:
    print("Y_COL is numeric")
else:
    # Removes commas
    data[Y_COL] = df[Y_COL].str.replace(",", "")
    # Converts data to numeric
    data[Y_COL] = pd.to_numeric(data[Y_COL], errors="coerce")
print(data[Y_COL].dtype)

# Drops rows if X or Y values are missing after data conversion
data = data.dropna()
print("Kept from csv" + str(len(data)) + " rows out of " + str(len(df)) + "\nrows")

# Filters rows from user-inputted numeric ranges
in_range = (
    (data[X_COL] >= X_MIN_FLT) & (data[X_COL] <= X_MAX_FLT)
    & (data[Y_COL] >= Y_MIN_FLT) & (data[Y_COL] <= Y_MAX_FLT)
)
data_filtered = data[in_range]
print("Kept " + str(len(data_filtered)) + " rows out of " + str(len(data)) + "\nrows")

# Prompts user to input customization on scatterplots
vs_linewidth= input("\nEnter the linewidth (default is 0.3): ")
if not vs_linewidth:
    print("Defaulting to 0.3")
    var_linewidth=0.3
else:
    var_linewidth=float(vs_linewidth)

var_edgecolor= input("\nEnter the edge color (default is red): ")
if not var_edgecolor:
    print("Defaulting to red")
    var_edgecolor="red"

var_set_title= input("\nEnter the title you want displayed (default is auto-generated): ")
if not var_set_title:
    var_set_title=f"{Y_COL} vs. {X_COL} (n = {len(data_filtered)})"

var_olscolor = input("\nEnter the color of the OLS line (default is crimson): ")
if not var_olscolor:
    var_olscolor="crimson"

var_olslinewidth = input("\nEnter the linewidth of the OLS line (default is 2): ")
if not var_olslinewidth:
    var_olslinewidth=2.0

# 6. Create scatterplot without regression line
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(
    data_filtered[X_COL],
    data_filtered[Y_COL],
    alpha=0.6,
    edgecolor=var_edgecolor,
    linewidth=var_linewidth
)

ax.set_xlabel(X_COL)
ax.set_ylabel(Y_COL)
ax.set_title(var_set_title)
ax.grid(alpha=0.3)
fig.tight_layout()

# 7. Ask user whether to save scatterplot
save_scatter = input("\nSave scatterplot? (yes/no): ").lower()

if save_scatter == "yes":
    scatter_file = input("Enter scatterplot file name (.png): ")
    fig.savefig(scatter_file, dpi=300)
    print(f"Saved scatterplot -> {scatter_file}")


# 8. Perform OLS linear regression
X = sm.add_constant(data_filtered[X_COL])
model = sm.OLS(data_filtered[Y_COL], X).fit()

# Displays regression summary and statistics
print("\nOLS Regression Summary:")
print(model.summary())

print(f"Intercept (β0): {model.params['const']:.4f}")
print(f"Slope (β1): {model.params[X_COL]:.4f}")
print(f"R-squared: {model.rsquared:.4f}")


# 9. Add regression line to scatterplot
x_line = np.linspace(
    data_filtered[X_COL].min(),
    data_filtered[X_COL].max(),
    100
)

y_line = (
    model.params["const"]
    + model.params[X_COL] * x_line
)

# Plots regression line on the scatterplot
ax.plot(
    x_line,
    y_line,
    color=var_olscolor,
    linewidth=var_olslinewidth,
    label=f"OLS line (R² = {model.rsquared:.3f})"
)

ax.set_title(var_set_title +" with OLS line")
ax.legend()
fig.tight_layout()


# 10. Ask user whether to save regression plot
save_ols = input("\nSave scatterplot with OLS line? (yes/no): ").lower()

if save_ols == "yes":
    ols_file = input("Enter regression plot file name (.png): ")
    fig.savefig(ols_file, dpi=300)
    print(f"Saved scatterplot with OLS line -> {ols_file}")

# Displays final plot
plt.show()