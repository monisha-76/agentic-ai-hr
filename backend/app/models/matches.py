from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
from bson import ObjectId

# Load environment variables
load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

# Build Atlas URI (same as job_description.py)
MONGO_URI = (
    f"mongodb+srv://{MONGO_USERNAME}:"
    f"{MONGO_PASSWORD}@{MONGO_CLUSTER}/"
    f"{MONGO_DB_NAME}?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

matches_collection = db["matches"]


def save_match(resume_id, matches):
    """
    Save JD match results for a resume.
    """
    match_doc = {
        "resume_id": ObjectId(resume_id),
        "matches": matches,
        "created_at": datetime.utcnow()
    }
    return matches_collection.insert_one(match_doc).inserted_id


def get_matches_for_resume(resume_id):
    """Fetch all match documents for a resume"""
    return list(
        matches_collection.find({"resume_id": ObjectId(resume_id)})
    )


def get_matches_for_jd(jd_id):
    """Fetch all resumes matched to a JD"""
    return list(
        matches_collection.find({"matches.jd_id": jd_id})
    )
