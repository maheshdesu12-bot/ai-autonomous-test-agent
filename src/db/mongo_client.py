from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not set in environment")

# Detect if using MongoDB Atlas
if "mongodb+srv" in MONGO_URI:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where()
    )
else:
    # Local MongoDB (GitHub Actions service container)
    client = MongoClient(MONGO_URI)

db = client.get_database()

users_collection = db["users"]

# Safe connection check
try:
    client.admin.command("ping")
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection failed:", e)
    raise