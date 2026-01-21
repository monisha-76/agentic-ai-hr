from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from app.config import database
from app.models.job_description import create_jd, get_all_jds
from app.skill_extraction_agent import resumes_collection
from app.agents.jd_matching_agent import JDMatchingAgent
from app.models.matches import save_match, get_match_count_per_jd
from app.agents.jd_skill_extraction_agent import JDSkillExtractionAgent

router = APIRouter(
    prefix="/jd",
    tags=["Job Description"]
)

# Mongo collection
jd_collection = database["job_descriptions"]
matches_collection = database["matches"]

# Agents
match_agent = JDMatchingAgent()
jd_skill_agent = JDSkillExtractionAgent()


# ===============================
# CREATE JOB DESCRIPTION
# ===============================
@router.post("/create")
def add_job_description(
    title: str = Body(..., example="Senior Python Developer"),
    description: str = Body(..., example="We need a Python dev with FastAPI experience")
):
    if not title or not description:
        raise HTTPException(status_code=400, detail="Title and description are required")

    # Extract skills from JD text
    skills = jd_skill_agent.extract_skills(description)

    jd_id = create_jd(title, description, skills)

    return {
        "message": "Job description created",
        "jd_id": str(jd_id),
        "skills": skills
    }


# ===============================
# GET ALL JOB DESCRIPTIONS
# (Frontend-friendly with matched_profiles)
# ===============================
@router.get("/all")
async def list_all_jds():
    jds = get_all_jds()  # list of all JDs
    match_counts = await get_match_count_per_jd()  # dict JD ID → number of matched resumes

    # Add `matched_profiles` field to each JD
    for jd in jds:
        jd_id = jd["_id"]
        jd["matched_profiles"] = match_counts.get(jd_id, 0)

    return jds


# ===============================
# DELETE JOB DESCRIPTION
# ===============================
@router.delete("/delete/{jd_id}")
async def delete_jd(jd_id: str):
    try:
        result = await jd_collection.delete_one({"_id": ObjectId(jd_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JD ID")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job Description not found")

    return {"message": "Job Description deleted successfully"}


# ===============================
# MATCH ONE RESUME TO ALL JDs
# ===============================
@router.get("/match/{resume_id}")
def match_resume_to_jd(resume_id: str, top_k: int = 3):

    resume = resumes_collection.find_one({"_id": ObjectId(resume_id)})

    if not resume or "skills" not in resume:
        raise HTTPException(status_code=400, detail="Resume not processed or skills missing")

    resume_skills = resume["skills"]

    jds = get_all_jds()
    if not jds:
        return {"message": "No job descriptions available"}

    matches = match_agent.match_resume_to_jds(resume_skills, jds, top_k)

    save_match(resume_id, matches)

    return {
        "resume_id": resume_id,
        "matches": matches
    }


# ===============================
# MATCH ALL RESUMES TO ALL JDs
# ===============================
@router.post("/match_all")
def match_all_resumes(top_k: int = 3):

    jds = get_all_jds()
    if not jds:
        raise HTTPException(status_code=400, detail="No job descriptions available")

    total_matched = 0

    for resume in resumes_collection.find({"skills": {"$exists": True}}):
        resume_id = str(resume["_id"])
        resume_skills = resume["skills"]

        matches = match_agent.match_resume_to_jds(resume_skills, jds, top_k)
        save_match(resume_id, matches)
        total_matched += 1

    return {
        "message": "All resumes matched successfully",
        "total_resumes_matched": total_matched
    }