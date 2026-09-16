import requests

# A Census API URL always has this shape:
# https://api.census.gov/data/{year}/{dataset}?get={variables}&for={geography}

YEAR = 2020
DATASET = "dec/pl"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "ba8547cb59e186c6969dd8d4e1c59556c026881a"

params = {
    "get": "NAME,P1_001N", # NAME = state name, B01003_001E = total population
    "for": "state:*",           # means "every state"
    "key": API_KEY,
}

response = requests.get(URL, params=params)
#response.raise_for_status()
if response.status_code != 200:
    print(f"Request failed({response.status_code})")
    print(response.text)
    raise SystemExit(1)

data = response.json()

# The API returns a list of lists. The first row is the column headers.
# [1:] returns from 1 to the end of the list


print(f"Got {len(data) - 1} rows back.")

for i in data:
    print(i)