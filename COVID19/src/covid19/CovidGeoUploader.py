"""
CovidGeoUploader: Geocodes Toronto neighbourhoods from a CSV file and uploads the coordinates to MongoDB.

This script:
1. Loads a list of Toronto neighbourhood names from a CSV file.
2. Uses the Nominatim OpenStreetMap API to fetch latitude and longitude for each neighbourhood.
3. Stores the results in a MongoDB collection on MongoDB Atlas.

Ensure that:
- The CSV file is located at /data/COVID19 cases.csv relative to this script.
- MongoDB Atlas URI is correct.
- Nominatim's usage policy (1 request/second) is respected.
"""

import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient

class CovidGeoUploader:
    def __init__(self, csv_filename, atlas_uri, db_name, collection_name):
        load_dotenv()
        self.csv_path = Path(__file__).resolve().parent / "data" / csv_filename
        self.atlas_uri = atlas_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(self.atlas_uri)
        self.db = self.client[self.db_name]

    def load_neighbourhoods(self):
        df = pd.read_csv(self.csv_path)
        return sorted(df["Neighbourhood Name"].dropna().unique())

    def geocode_neighbourhoods(self, neighbourhoods):
        results = []
        headers = {"User-Agent": "covid-geo-uploader/1.0 (your_email@example.com)"}
        for name in neighbourhoods:
            name_clean = name.strip()
            query = f"{name_clean}, Toronto, Ontario, Canada"
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": query,
                "format": "json",
                "limit": 1
            }

            print(f"Querying: {query}")
            try:
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        lat = float(data[0]['lat'])
                        lon = float(data[0]['lon'])
                        print(f"Found: {name_clean} => {lat}, {lon}")
                        results.append({"neighbourhood": name_clean, "latitude": lat, "longitude": lon})
                    else:
                        print(f"No coordinates found for {name_clean}")
                        results.append({"neighbourhood": name_clean, "latitude": None, "longitude": None})
                else:
                    print(f"HTTP Error {response.status_code} for {name_clean}")
                    results.append({"neighbourhood": name_clean, "latitude": None, "longitude": None})
            except Exception as e:
                print(f"Exception while geocoding {name_clean}: {e}")
                results.append({"neighbourhood": name_clean, "latitude": None, "longitude": None})

            time.sleep(1.0)  # Respect Nominatim's 1 request/sec limit
        return results

    def upload_to_mongodb(self, documents):
        collection = self.db[self.collection_name]
        result = collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents into the {self.collection_name} collection.")

    def run(self):
        print("Loading neighbourhoods...")
        neighbourhoods = self.load_neighbourhoods()
        print(f"Geocoding {len(neighbourhoods)} neighbourhoods...")
        coordinates = self.geocode_neighbourhoods(neighbourhoods)
        print("Uploading to MongoDB...")
        self.upload_to_mongodb(coordinates)
        print("All done!")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    uploader = CovidGeoUploader(
        csv_filename="COVID19 cases.csv",
        atlas_uri="mongodb+srv://as:123@cluster0.7nmgzr1.mongodb.net/",
        db_name="CovidDB",
        collection_name="Neighbourhoods"
    )
    uploader.run()
