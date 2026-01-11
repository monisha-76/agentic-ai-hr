from fastapi import APIRouter, Depends, HTTPException
from app.config import database
from app.utils.jwt import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# Mongo collections
resumes_collection = database["resumes"]
jd_collection = database["job_descriptions"]
matches_collection = database["matches"]


@router.get("/stats")
async def get_admin_stats(current_user: dict = Depends(get_current_user)):

    # 🔐 ADMIN ONLY
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    total_resumes = await resumes_collection.count_documents({})
    total_jds = await jd_collection.count_documents({})
    matched_profiles = await matches_collection.count_documents({})

    return {
        "total_resumes": total_resumes,
        "total_jds": total_jds,
        "matched_profiles": matched_profiles
    }