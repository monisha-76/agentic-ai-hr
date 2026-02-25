from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.config import database
from app.utils.jwt import get_current_user

router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"]
)

# -------------------
# Collections
# -------------------
resumes_collection = database["resumes"]
jd_collection = database["job_descriptions"]
profiles_collection = database["profiles"]


# ===============================
# 📊 Candidate Dashboard Stats
# ===============================
@router.get("/stats")
async def get_candidate_stats(current_user: dict = Depends(get_current_user)):

    # 🔐 Candidate only
    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    total_jobs = await jd_collection.count_documents({})

    my_applications = await resumes_collection.count_documents({
        "candidate_id": current_user["id"]
    })

    total_applications = await resumes_collection.count_documents({})

    return {
        "total_jobs": total_jobs,
        "myApplications": my_applications,
        "totalApplications": total_applications
    }


# ===========
# ====================
# 📄 My Applications List
# ===============================
@router.get("/applications")
async def get_my_applications(current_user: dict = Depends(get_current_user)):

    # 🔐 Candidate only
    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    resumes = await resumes_collection.find({
        "candidate_id": current_user["id"]
    }).to_list(length=None)

    applications = []

    for resume in resumes:

        jd = await jd_collection.find_one({
            "_id": ObjectId(resume["jd_id"])
        })

        if jd:
            applications.append({
                "resume_id": str(resume["_id"]),
                "jd_id": str(jd["_id"]),
                "title": jd["title"],
                "skills": jd.get("skills", []),
                "applied_at": resume.get("created_at")
            })

    return applications
