#####################################################
#   Lab 9: Logistic and Count-Variable Regression   #
# --------------------------------------------------#
#     Remington Bland # HSC4933.005 # 10/25/26      #
#                   blandr@usf.edu                  #
#####################################################

# Imports
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools import add_constant
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from pathlib import Path
import sys

# Function defined to help determine if column is numeric
def to_numeric_column(frame, col):
    if pd.api.types.is_numeric_dtype(frame[col]):
        return True, frame[col]

    # Converts from text that contains numbers
    converted = pd.to_numeric(frame[col].str.replace(",", ""), errors="coerce")

    # Columns remain non-numeric if truly non-numeric
    if converted.isna().all():
        return False, None

    return True, converted

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

# Prompt the user to choose the type of model
while True:
    mode = input("Model type (l=logistic / c=count): ").strip().lower()

    if not mode:
        print("No model type entered. Exiting.")

    if mode in ("l", "c"):
        break

    print("Error: type 'l' or 'c'. Try again.")

# Load the dataset
df = pd.read_csv(filename)

# Clean column names to snake_case
df.columns = (df.columns.str.lower().str.replace(" ", "_"))

# List available column names
print("\nAvailable columns:")
print(df.columns.tolist())

# Asks for the y column
while True:
    y_col = input("Choose the y column: ").strip()

    # No columns were entered
    if not y_col:
        print("No column entered.")
        sys.exit()

    # If column name does not exist
    if y_col not in df.columns:
        print("Error: '" + y_col + "' is not a valid column name. Try again.")
        continue

    ok, predictors = to_numeric_column(df, y_col)
    if not ok:
        print("Error: '" + y_col + "' is not numeric. Pick a number column.")
        continue

    # Keeps numeric version
    df[y_col] = predictors
    break

# Asks for the x columns as the predictors
print()
print("Enter the x columns one at a time.")
print("Press Enter on a blank line when you are done (at least one required).")

# Empty array list
x_cols = []

while True:
    x_col = input("Choose the x column (blank to finish): ").strip()
    if not x_col:
        if not x_cols:
            # Blank at the first entry
            print("No x column entered.")
            sys.exit()
        break

    # Rejects column name if not a real column
    if x_col not in df.columns:
        print("Error: '" + x_col + "' is not a valid column name. Try again.")
        continue

    # Rejects column name if column is chosen for y
    if x_col == y_col:
        print("Error: '" + x_col + "' is the y column. Try again.")
        continue

    # Rejects a x column already added (no same x is plotted twice)
    if x_col in x_cols:
        print("Error: '" + x_col + "' is already in the list. Pick another one.")
        continue

    # Try to use as numbers as in the x column
    ok, predictors = to_numeric_column(df, x_col)
    if not ok:
        print("Error: '" + x_col + "' is not numeric. Pick a number column.")
        continue

    # Keeps numeric version
    df[x_col] = predictors
    x_cols.append(x_col)
    print("Added '" + x_col + "'. (" + str(len(x_cols)) + " so far)")

print()
print("Plotting these X columns against '" + y_col + "': " + ", ".join(x_cols))

# Removes rows missing any of the values
needed = [y_col] + x_cols
rows_before = len(df)
data = df.dropna(subset=needed)
skipped = rows_before - len(data)

# Displays rows skipped
if skipped > 0:
    print()
    print("Skipped "+ str(skipped) + " row(s) missing the target or a predictor")

    if len(data) == 0:
        print("No rows left. Exiting.")
        sys.exit()

# Plotting out the count-variable regression model
if mode == "c":

    # Scale predictors
    df_scaled = data.copy()
    for col in x_cols:
        df_scaled[col] = (df_scaled[col] - df_scaled[col].mean()) / df_scaled[col].std()

    # Calculate and display VIF
    X = add_constant(df_scaled[x_cols])
    vif_df = pd.DataFrame()
    vif_df["Feature"] = X.columns
    vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print(vif_df.to_string(index=False))
    print("-" * 40)

    # Make formula
    formula = y_col + ' ~ ' + ' + '.join(x_cols)

    # Run model
    print("Fitting model...")
    model = smf.poisson(formula, data=df_scaled).fit()

    # Print model summary
    print(model.summary())
    # Prompts the user to save file
    output_filename = input("Enter the output file name (or press Enter to skip): ").strip()

    if output_filename:
      with open(output_filename, "w") as f:
          f.write(str(model.summary()))

# Plotting out the logistic model
if mode == "l":

    # Predictors X and y
    X = data[x_cols]
    y = data[y_col]

    # Training and testing sets
    print("Calling train_test_split")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Logistic Regression model
    print("Calling Logistic Regression")
    model = LogisticRegression(solver='lbfgs', max_iter=1000)

    # Train (fit) the model using training data
    print("Calling model fit")
    model.fit(X_train, y_train)

    # Make predictions on the test set
    print("Calling model predict\n")
    y_pred = model.predict(X_test)

    # Optional probabilities: view actual predicted probabilities
    probabilities = model.predict_proba(X_test)

    # Accuracy of linear regression
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy:  {accuracy:.2%}")

    # Print classification report
    print(classification_report(y_test, y_pred))
    cr = classification_report(y_test, y_pred)

    # Compute the confusion matrix array
    print("Calling confusion matrix")
    cm = confusion_matrix(y_test, y_pred)

    print("Calling Confusion Matrix Display")
    # Display the formatted matrix cleanly with default lables (0 and 1)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    # Prompts the user to save file
    output_filename = input("Enter the output file name (or press Enter to skip): ").strip()

    # Saves to a text file
    if output_filename:
      with open(output_filename, "w") as f:
          f.write("Logic Regression Classification Report\n")
      with open (output_filename, "a") as f:
          f.write(str(cr))
          f.write("\n\n\nConfusion Matrix\n")
          f.write(str(cm))