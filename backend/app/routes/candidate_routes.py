from fastapi import APIRouter, Depends, HTTPException
from app.config import database
from app.utils.jwt import get_current_user

router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"]
)

resumes_collection = database["resumes"]
jd_collection = database["job_descriptions"]

@router.get("/stats")
async def get_candidate_stats(current_user: dict = Depends(get_current_user)):

    # 🔐 CANDIDATE ONLY
    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    # Total JDs (for browsing)
    total_jobs = await jd_collection.count_documents({})

    # My Applications (resumes uploaded by this candidate)
    my_applications = await resumes_collection.count_documents({
        "candidate": current_user["id"]
    })

    # Total Applications (all resumes in system)
    total_applications = await resumes_collection.count_documents({})

    return {
        "total_jobs": total_jobs,
        "myApplications": my_applications,
        "totalApplications": total_applications
    }