# app/models/job_description.py
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

# Build Atlas URI
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

job_descriptions_collection = db["job_descriptions"]


def create_jd(title: str, description: str, skills: list = None):
    if skills is None:
        skills=[]
    """
    Create a new Job Description in MongoDB.
    """
    jd = {
        "title": title,
        "description": description,
        "skills": skills,
        "created_at": datetime.utcnow()
    }
    return job_descriptions_collection.insert_one(jd).inserted_id


def get_all_jds():
    """Return all Job Descriptions as a list"""
    jds = []
    for jd in job_descriptions_collection.find():
        jd["_id"] = str(jd["_id"])  # JSON safe
        jds.append(jd)
    return jds


def get_jd_by_id(jd_id):
    """Fetch a single JD by MongoDB _id"""
    return job_descriptions_collection.find_one({"_id": ObjectId(jd_id)})