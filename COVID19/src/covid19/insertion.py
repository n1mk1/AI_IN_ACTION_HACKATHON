import csv
from pymongo import MongoClient
from pathlib import Path
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb+srv://as:<pass>@cluster0.7nmgzr1.mongodb.net/")
db = client["CovidDB"]
collection = db["CovidCases"]

# Construct the path to the CSV
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "data" / "COVID19 cases.csv"

# Read and convert CSV data
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    records = list(reader)

# Convert string to datetime safely
def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except:
        return None

# Clean and convert each record
cleaned_records = []
for doc in records:
    cleaned_doc = {
        "_id": int(doc["_id"]),
        "Assigned_ID": int(doc["Assigned_ID"]),
        "Outbreak_Associated": doc["Outbreak Associated"].strip(),
        "Age_Group": doc["Age Group"].strip(),
        "Neighbourhood_Name": doc["Neighbourhood Name"].strip(),
        "FSA": doc["FSA"].strip(),
        "Source_of_Infection": doc["Source of Infection"].strip(),
        "Classification": doc["Classification"].strip(),
        "Episode_Date": parse_date(doc["Episode Date"]),
        "Reported_Date": parse_date(doc["Reported Date"]),
        "Client_Gender": doc["Client Gender"].strip(),
        "Outcome": doc["Outcome"].strip(),
        "Ever_Hospitalized": doc["Ever Hospitalized"].strip().lower() == "yes",
        "Ever_in_ICU": doc["Ever in ICU"].strip().lower() == "yes",
        "Ever_Intubated": doc["Ever Intubated"].strip().lower() == "yes"
    }
    cleaned_records.append(cleaned_doc)

# Insert into MongoDB
collection.insert_many(cleaned_records)

print(f"Inserted {len(cleaned_records)} records into MongoDB.")
