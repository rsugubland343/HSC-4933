######################################
#     Lab 7: # Linear Regression     #
#      Jordan Beaird  10/11/2026     #
#------------------------------------#
#           Beaird@usf.edu           #
#------------------------------------#
#          Linear Regression         #
######################################
# HSC 4933 - Lab 7 Linear Regression #

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


# 1. Prompt user for dataset and load CSV
CSV_PATH = input("Enter the CSV dataset file name: ")
df = pd.read_csv(CSV_PATH)


# 2. Clean column names to snake_case
df.columns = (df.columns.str.lower().str.replace(" ", "_")
)


# 3. List available column names
print("\nAvailable columns:")
print(df.columns.tolist())


# 4. Prompt user for X and Y variables
X_COL = input("\nEnter the X variable: ").strip().lower()
Y_COL = input("Enter the Y variable: ").strip().lower()


# 5. Remove rows missing X or Y values
data = df[[X_COL, Y_COL]].copy()

data[X_COL] = pd.to_numeric(data[X_COL], errors="coerce")
data[Y_COL] = pd.to_numeric(data[Y_COL], errors="coerce")

data = data.dropna()


# 6. Create scatterplot without regression line
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(
    data[X_COL],
    data[Y_COL],
    alpha=0.6,
    edgecolor="k",
    linewidth=0.3
)

ax.set_xlabel(X_COL)
ax.set_ylabel(Y_COL)
ax.set_title(f"{Y_COL} vs. {X_COL} (n = {len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()


# 7. Ask user whether to save scatterplot
save_scatter = input("\nSave scatterplot? (yes/no): ").lower()

if save_scatter == "yes":
    scatter_file = input("Enter scatterplot file name (.png): ")
    fig.savefig(scatter_file, dpi=300)
    print(f"Saved scatterplot -> {scatter_file}")


# 8. Perform OLS linear regression
X = sm.add_constant(data[X_COL])
model = sm.OLS(data[Y_COL], X).fit()

print("\nOLS Regression Summary:")
print(model.summary())

print(f"Intercept (β0): {model.params['const']:.4f}")
print(f"Slope (β1): {model.params[X_COL]:.4f}")
print(f"R-squared: {model.rsquared:.4f}")


# 9. Add regression line to scatterplot
x_line = np.linspace(
    data[X_COL].min(),
    data[X_COL].max(),
    100
)

y_line = (
    model.params["const"]
    + model.params[X_COL] * x_line
)

ax.plot(
    x_line,
    y_line,
    color="crimson",
    linewidth=2,
    label=f"OLS line (R² = {model.rsquared:.3f})"
)

ax.set_title(
    f"{Y_COL} vs. {X_COL} with OLS line (n = {len(data)})"
)

ax.legend()
fig.tight_layout()


# 10. Ask user whether to save regression plot
save_ols = input(
    "\nSave scatterplot with OLS line? (yes/no): "
).lower()

if save_ols == "yes":
    ols_file = input("Enter regression plot file name (.png): ")
    fig.savefig(ols_file, dpi=300)
    print(f"Saved scatterplot with OLS line -> {ols_file}")

plt.show()