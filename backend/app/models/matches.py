from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

MONGO_URI = (
    f"mongodb+srv://{MONGO_USERNAME}:"
    f"{MONGO_PASSWORD}@{MONGO_CLUSTER}/"
    f"{MONGO_DB_NAME}?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

matches_collection = db["matches"]


def save_match(resume_id, matches):
    match_doc = {
        "resume_id": ObjectId(resume_id),
        "matches": matches,
        "created_at": datetime.utcnow()
    }
    return str(matches_collection.insert_one(match_doc).inserted_id)


def serialize_match(doc):
    doc["_id"] = str(doc["_id"])
    doc["resume_id"] = str(doc["resume_id"])
    return doc


def get_matches_for_resume(resume_id):
    results = matches_collection.find(
        {"resume_id": ObjectId(resume_id)}
    )
    return [serialize_match(doc) for doc in results]


def get_matches_for_jd(jd_id):
    results = matches_collection.find(
        {"matches.jd_id": ObjectId(jd_id)}
    )
    return [serialize_match(doc) for doc in results]

def get_match_count_per_jd():
    """
    Returns a dictionary of JD ID → number of matched resumes
    """
    pipeline = [
        {"$unwind": "$matches"},  # flatten matches array
        {"$group": {
            "_id": "$matches.jd_id",
            "count": {"$sum": 1}
        }}
    ]
    results = list(matches_collection.aggregate(pipeline))
    
    # Convert ObjectId to string
    match_count = {}
    for r in results:
        match_count[str(r["_id"])] = r["count"]
    return match_count