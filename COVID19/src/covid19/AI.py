import pymongo
from sentence_transformers import SentenceTransformer
import numpy as np

# Setup
client = pymongo.MongoClient("mongodb+srv://as:123@cluster0.7nmgzr1.mongodb.net/")
db = client["CovidDB"]
collection = db["CovidCases"]
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


