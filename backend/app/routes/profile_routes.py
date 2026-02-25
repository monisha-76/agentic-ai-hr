from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId

from app.config import database
from app.utils.jwt import get_current_user

router = APIRouter(
    prefix="/candidate",
    tags=["Candidate Profile"]
)

profiles_collection = database["profiles"]


# ===============================
# 📥 GET PROFILE
@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):

    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    profile = await profiles_collection.find_one({
        "candidate_id": current_user["id"]
    })

    if not profile:
        return {}

    profile["_id"] = str(profile["_id"])
    return profile



# ===============================
# 📤 CREATE / UPDATE PROFILE
# ===============================
@router.put("/profile")
async def create_or_update_profile(
    data: dict,
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    existing_profile = await profiles_collection.find_one({
        "candidate_id": current_user["id"]
    })

    profile_data = {
        "candidate_id": current_user["id"],
        "full_name": data.get("full_name"),
        "gender": data.get("gender"),
        "phone": data.get("phone"),
        "degree": data.get("degree"),
        "university": data.get("university"),
        "cgpa": data.get("cgpa"),
        "year_of_passing": data.get("year_of_passing"),
        "skills": data.get("skills", []),
        "experience": data.get("experience", {}),
        "linkedin": data.get("linkedin"),
        "github": data.get("github"),
        "resume_url": data.get("resume_url"),
        "updated_at": datetime.utcnow()
    }

    if existing_profile:
        await profiles_collection.update_one(
            {"candidate_id": current_user["id"]},
            {"$set": profile_data}
        )
        return {"message": "Profile updated successfully"}

    else:
        profile_data["created_at"] = datetime.utcnow()
        await profiles_collection.insert_one(profile_data)
        return {"message": "Profile created successfully"}
