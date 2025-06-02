from pymongo import MongoClient

ATLAS_URI = "mongodb+srv://as:123@cluster0.7nmgzr1.mongodb.net/"
DB_NAME = "CovidDB"
COLLECTION_NAME = "CovidCases"

class AtlasClient:

    def __init__(self, atlas_uri, dbname):
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]

    def ping(self):
        self.mongodb_client.admin.command("ping")

    def get_collection(self, collection_name):
        return self.database[collection_name]

    def find(self, collection_name, filter={}, limit=0):
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items

# ======= MAIN EXECUTION BLOCK =======

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()
print("Connected to Atlas instance! We are good to go!")

print("======== Finding some sample COVID cases ========================")

cases = atlas_client.find(collection_name=COLLECTION_NAME, limit=5)

print(f"Found {len(cases)} COVID case records")
for idx, case in enumerate(cases):
    print(
        f"""{idx+1}
        id: {case.get('Assigned_ID')}
        Neighbourhood: {case.get('Neighbourhood_Name')}
        Gender: {case.get('Client_Gender')}
        Age Group: {case.get('Age_Group')}
        Episode Date: {case.get('Episode_Date')}
        Reported Date: {case.get('Reported_Date')}
        Classification: {case.get('Classification')}
        Outcome: {case.get('Outcome')}
        Source of Infection: {case.get('Source_of_Infection')}
        """
    )
print("================================")

