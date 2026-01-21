# app/models/matches.py
from app.config import database
from bson import ObjectId
from datetime import datetime

matches_collection = database["matches"]  # Motor collection

async def save_match(resume_id, candidate_name, candidate_email, jd_id, match_result):
    """
    Save a single match document for a resume & JD.
    match_result should already contain: score, rank, matched_skills, extra_skills
    """
    match_doc = {
        "resume_id": ObjectId(resume_id),
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "jd_id": ObjectId(jd_id),
        "matches": [match_result],
        "created_at": datetime.utcnow()
    }
    result = await matches_collection.insert_one(match_doc)
    return str(result.inserted_id)


def serialize_match(doc):
    doc["_id"] = str(doc["_id"])
    doc["resume_id"] = str(doc["resume_id"])
    doc["jd_id"] = str(doc["jd_id"])
    return doc


async def get_matches_for_resume(resume_id):
    cursor = matches_collection.find({"resume_id": ObjectId(resume_id)})
    results = await cursor.to_list(length=None)
    return [serialize_match(doc) for doc in results]


async def get_matches_for_jd(jd_id):
    cursor = matches_collection.find({"jd_id": ObjectId(jd_id)})
    results = await cursor.to_list(length=None)
    return [serialize_match(doc) for doc in results]


async def get_match_count_per_jd():
    pipeline = [
        {"$unwind": "$matches"},
        {"$group": {"_id": "$jd_id", "count": {"$sum": 1}}}
    ]
    cursor = matches_collection.aggregate(pipeline)
    results = await cursor.to_list(length=None)

    match_count = {str(r["_id"]): r["count"] for r in results}
    return match_count
