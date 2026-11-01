########################################
#     Lab 10: Survival Analysis Lab    #
# -------------------------------------#
#      Remington Bland # 11/1/2026     #
#     HSC4933.005 # blandr@usf.edu     #
########################################

# Imports
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test
#from scipy.stats import logrank

# Specify Data Files
csv_lr_file_path = "km_logrank_readmission.csv"

# Specify Column Names
time_column = "time_days"
event_column = "readmitted"

# Load Data
dflr= pd.read_csv(csv_lr_file_path)

print("I have read the file")
print(dflr[time_column].dtype)
print(dflr[event_column].dtype)

# Initialize the fitter
kmf = KaplanMeierFitter()
fig, ax = plt.subplots(figsize=(10, 6))

logrank_result = None

# Plot Curve(s)


# Option B -> Plot a single curve for the entire dataset
kmf.fit(
    durations=dflr[time_column],
    event_observed=dflr[event_column],
    label="Full Cohort",
)


kmf.plot_survival_function(ax=ax, show_censors=True)

# Annotate plot with log-rank p-value
if logrank_result is not None:
    p = logrank_result.p_value
    p_text = "p < 0.001" if p < 0.001 else f"p = {p:.3f}"
    ax.text(
        0.97, 0.97,
        f"Log-rank test\n{p_text}",
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

# Plot Formatting
plt.title("Kaplan-Meier Survival Curve", fontsize=14)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Survival Probability", fontsize=12)
plt.ylim(0, 1.05)  # Constrain y-axis from 0% to 100%
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(loc="lower left")
plt.tight_layout()

# Save Plot
plt.savefig("logrank_readmission.png")

# Cox heart failure plot
csv_cox_file_path = "cox_ph_heart_failure_survival.csv"

# Specify Column names
time_column = "time_months"
event_column = "death"
continuous_covariates = ["age", "bmi", "systolic_bp", "ejection_fraction"]
binary_covariates = ["sex", "diabetes", "smoker", "chronic_kidney_disease", "beta_blocker"]
ordinal_covariates = ["nyha_class"]  # dummy-coded; first level is reference

# Load Data
dfph= pd.read_csv(csv_cox_file_path)
print("I have read the file")
print(dfph[time_column].dtype)
print(dfph[event_column].dtype)
# Prepare Model Data
# Convert booleans (True/False or "True"/"False") to 0/1
for col in binary_covariates:
    dfph[col] = dfph[col].astype(str).str.strip().str.lower().isin(["true", "1", "yes", "male"]).astype(int)

model_df = dfph[[time_column, event_column] + continuous_covariates + binary_covariates + ordinal_covariates]
model_df = pd.get_dummies(model_df, columns=ordinal_covariates, drop_first=True, dtype=int)
model_df = model_df.dropna()

print(len(model_df))

# Fit Cox Proportional Hazards Model
cph = CoxPHFitter()
cph.fit(model_df, duration_col=time_column, event_col=event_column)

# Results
cph.print_summary(decimals=3)  # coef, HR (exp(coef)), 95% CI, p-values, concordance
print(f"\nConcordance index: {cph.concordance_index_:.3f}")

# Check Proportional Hazards Assumption
# Prints Schoenfeld-residual-based tests; low p-values flag possible violations
print("\n--- Proportional hazards assumption check ---")
cph.check_assumptions(model_df, p_value_threshold=0.05, show_plots=False)

# Plot 1: Hazard Ratios (forest plot)
fig, ax = plt.subplots(figsize=(8, 5))
cph.plot(hazard_ratios=True, ax=ax)
ax.axvline(1, color="gray", linestyle="--")
ax.set_title("Cox PH Model: Hazard Ratios (95% CI)", fontsize=14)
ax.set_xlabel("Hazard Ratio", fontsize=12)
plt.tight_layout()
plt.savefig("cox_hazard_ratios.png")

# Display Plots
plt.show()