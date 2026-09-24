# Import libs
import json
import datetime
import os
from anonymate.anonymizer import Anonymizer
from cryptography.fernet import Fernet
from decimal import Decimal

# Data from the given 5 profiles
profiles = [
    {
        'job': 'Agricultural engineer',
        'company': 'Phillips-Johnson',
        'ssn': '055-51-3629',
        'residence': '1107 Brian Coves\nSouth Jessica, UT 66862',
        'current_location': (Decimal('-81.6575675'), Decimal('111.794874')),
        'blood_group': 'B+', 'website': [
            'https://hurley.com/',
            'http://www.baker.info/',
            'http://silva-jones.com/',
            'https://www.mathews.com/'
        ],
        'username': 'nnelson',
        'name': 'Oscar Newman',
        'sex': 'M',
        'address': '2574 Scott Manors\nPort Aprilfort, MI 13337',
        'mail': 'wgraham@hotmail.com',
        'birthdate': datetime.date(1927, 1, 19)
    },
    {
        'job': 'Engineer, civil (consulting)',
        'company': 'Guzman Inc',
        'ssn': '457-09-3674',
        'residence': '8014 Lambert Ways Apt. 285\nSouth Briannaside, KS 13217',
        'current_location': (Decimal('61.686331'), Decimal('-42.036583')),
        'blood_group': 'A-',
        'website': [
            'http://gregory-martin.org/',
            'http://tanner.org/',
            'https://www.carr.org/'
        ],
        'username': 'lking',
        'name': 'Jeremy Wilson',
        'sex': 'M',
        'address': '9375 Thomas Alley Suite 536\nNorth Darren, AZ 22956',
        'mail': 'hdeleon@hotmail.com',
        'birthdate': datetime.date(1996, 10, 12)
    },
    {
        'job': 'Information officer',
        'company': 'Green Inc',
        'ssn': '230-42-2169',
        'residence': 'Unit 6625 Box 0858\nDPO AE 52466',
        'current_location': (Decimal('-78.802646'), Decimal('-47.996111')),
        'blood_group': 'A-',
        'website': [
            'https://www.watkins.com/',
            'http://johnson.org/'
        ],
        'username': 'timothycastro',
        'name': 'Kenneth Rhodes',
        'sex': 'M',
        'address': '7994 Pearson Square\nHannahmouth, FM 16699',
        'mail': 'sonya72@hotmail.com',
        'birthdate': datetime.date(2003, 6, 15)
    },
    {
        'job': 'Contracting civil engineer',
        'company': 'Smith-Williamson',
        'ssn': '796-76-1297',
        'residence': '0041 Brittany Mountains\nNorth Harryshire, MN 69202',
        'current_location': (Decimal('66.422320'), Decimal('107.124001')),
        'blood_group': 'AB+',
        'website': [
            'http://www.nolan.com/'
        ],
        'username': 'debraphillips',
        'name': 'Nicole Richardson',
        'sex': 'F',
        'address': '303 Wong Trafficway Suite 883\nLake Kiara, MN 78039',
        'mail': 'andrew33@gmail.com',
        'birthdate': datetime.date(2003, 9, 7)
    },
    {
        'job': 'Engineer, technical sales',
        'company': 'Moody-Meza',
        'ssn': '574-63-6422',
        'residence': '74438 Moore Fall\nSouth Andrew, GA 64257',
        'current_location': (Decimal('38.089195'), Decimal('35.459581')),
        'blood_group': 'A+',
        'website': [
            'https://brooks-moore.com/'
        ],
        'username': 'xlewis',
        'name': 'Gary Gamble',
        'sex': 'M',
        'address': '9929 Henderson Branch Suite 961\nLake Mary, AL 36478',
        'mail': 'ambercordova@yahoo.com',
        'birthdate': datetime.date(1968, 8, 19)
    }
]

# Encryption key is created
KEY_FILE = ("encryption.key")
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        encryption_key = f.read()
else:
    encryption_key: Fernet = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(encryption_key)

# Initialize anonymizer
anonymizer = Anonymizer(encryption_key=encryption_key)

# Patient data title displayed
print("Patient Data:")
print(profiles)

# Convert datat to json string
data_str = json.dumps(profiles, default=str)

# Run anonymizer
secure_data = anonymizer.encrypt_text(data_str)

# Show encrypted data
print("Encrypted Data:")
print(secure_data)

# Create boolean question function for file write
def write_to_file_question(question: str) -> bool:
    while True:
        write_decision = input(f"{question} (y/n): ")
        if write_decision in ('y', 'yes'):
            return True
        if write_decision in ('n', 'no'):
            return False
        print("Invalid input. Please enter 'y' or 'n'.")

write_bool = write_to_file_question("Would you like to write this data to file?")
if write_bool == True:
    custom_name = input("Enter the name for the file. (no special characters): ")

    file_name = (f"{custom_name}.txt")

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(secure_data)
    print(f"Saved to {file_name}")

else:
    print("Data not saved. All data will be lost when application is closed.")

# System created for queries

print("\nQuery Options:")
print("1. Name")
print("2. Date of Birth")
print("3. Sex")
print("4. Blood Type")

choice = input("Select an option (1-4): ")

profile_num = input("Enter the profile number (1-5): ")
if profile_num.isdigit():
    index = int(profile_num) - 1
    if index < 0 or index >= len(profiles):
        print("Invalid profile number. Please enter a valid profile number.")
    else:
        profile = profiles[index]

        if choice == 1:
            print(f"Name: {profile['first_name']}")
        elif choice == 2:
            print(f"Date of Birth: {profile['birthdate']}")
        elif choice == 3:
            print(f"Sex: {profile['sex']}")
        elif choice == 4:
            print(f"Blood Type: {profile['blood_group']}")
        else:
            print("Invalid query option.")
else:
    print("Profile number must be a digit.")