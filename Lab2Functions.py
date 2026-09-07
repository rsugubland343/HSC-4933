###################################################
#       Lab2Functions.py # blandr@usf.edu         #
###################################################
# (c) Remington Bland, 2026 # HSC4933 # Week 2    #
#    A script allowing input for patient dat      #
#    and stats, retrieving data on different      #
#           heart rates from patients             #
###################################################

# This is a dictionary of patient data:

heart_rate_samples = {
"J. Alvarez": [72, 75, 78],
"M. Chen": [80, 82],
"R. Okafor": [65, 68, 70, 66],
"S. Patel": [90, 95, 92, 88, 91],
"T. Nguyen": [77, 79],
"L. Kowalski": [68, 70, 69],
"D. Osei": [98, 101, 95, 99],
"A. Whitfield": [74, 76, 75, 73],
}

# Retrieves all the stats for a patient

def get_all_stats(name):
    """Return all heart-rate samples for a patient"""
    return heart_rate_samples.get(name)

def get_recent_stat(name):
    """Return the most recent heart-rate sample for a patient"""
    samples = heart_rate_samples.get(name)
    if samples:
        return samples[-1]
    return None

def get_mean_stat(name):
    """Return the average heart-rate sample for a patient"""
    samples = heart_rate_samples.get(name)
    if samples:
        return sum(samples) / len(samples)
    return None

def get_min_stat(name):
    """Return the minimum heart-rate sample for a patient"""
    samples = heart_rate_samples.get(name)
    if samples:
        return min(samples)
    return None

def get_max_stat(name):
    """Return the maximum heart-rate sample for a patient"""
    samples = heart_rate_samples.get(name)
    if samples:
        return max(samples)
    return None

print("Patient Heart-rate Lookup Dictionary")
print("-------------------------------------")

# Displays available patient names
print("Available patients:")
for patient in heart_rate_samples:
    print(patient)

# Asks user for a patient name
patient = input("\nEnter a patient's name as exactly as shown above: ")

# Displays options
print("\nChoose an option:")
print("1 - All stats")
print("2 - Recent stat")
print("3 - Average stat")
print("4 - Minimum stat")
print("5 - Maximum stat")

choice = int(input("Enter your choice: "))

# Calls the correct function
if choice == 1:
    result = get_all_stats(patient)
elif choice == 2:
    result = get_recent_stat(patient)
elif choice == 3:
    result = get_mean_stat(patient)
elif choice == 4:
    result = get_min_stat(patient)
elif choice == 5:
    result = get_max_stat(patient)
else:
    result = None

# Displays the result
if result is None:
    print("Invalid choice or patient is not found.")
else:
    print(f"Result for {patient}: {result}")
