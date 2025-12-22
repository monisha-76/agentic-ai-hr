from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId

from app.models.job_description import create_jd, get_all_jds
from app.skill_extraction_agent import resumes_collection
from app.agents.jd_matching_agent import JDMatchingAgent
from app.models.matches import save_match

# ✅ ADD THIS IMPORT
from app.agents.jd_skill_extraction_agent import JDSkillExtractionAgent


router = APIRouter(
    prefix="/jd",
    tags=["Job Description"]
)

# Agents
agent = JDMatchingAgent()
jd_skill_agent = JDSkillExtractionAgent()   # ✅ NEW


@router.post("/create")
def add_job_description(
    title: str = Body(..., example="Senior Python Developer"),
    description: str = Body(..., example="We need a Python dev with 5+ years experience...")
):
    """
    Create JD via Postman
    → Extract skills from JD
    → Store title, description, skills
    """

    if not title or not description:
        raise HTTPException(status_code=400, detail="Title and description are required")

    # ✅ EXTRACT SKILLS FROM JD TEXT
    skills = jd_skill_agent.extract_skills(description)

    # ✅ SAVE JD WITH SKILLS
    jd_id = create_jd(title, description, skills)

    return {
        "message": "Job description created",
        "jd_id": str(jd_id),
        "skills": skills
    }


@router.get("/all")
def list_all_jds():
    """Fetch all Job Descriptions"""
    jds = get_all_jds()
    return {"job_descriptions": jds}


@router.get("/match/{resume_id}")
def match_resume_to_jd(resume_id: str, top_k: int = 3):
    """
    Match ONE resume against ALL JDs
    """

    resume = resumes_collection.find_one({"_id": ObjectId(resume_id)})
    if not resume or "skills" not in resume:
        raise HTTPException(status_code=400, detail="Resume not processed or skills missing")

    resume_skills = resume["skills"]

    jds = get_all_jds()
    if not jds:
        return {"message": "No job descriptions available"}

    matches = agent.match_resume_to_jds(resume_skills, jds, top_k)

    save_match(resume_id, matches)

    return {"resume_id": resume_id, "matches": matches}


@router.post("/match_all")
def match_all_resumes(top_k: int = 3):
    """
    Match ALL resumes against ALL JDs
    """

    jds = get_all_jds()
    if not jds:
        raise HTTPException(status_code=400, detail="No job descriptions available")

    total_matched = 0

    for resume in resumes_collection.find({"skills": {"$exists": True}}):
        resume_id = str(resume["_id"])
        resume_skills = resume["skills"]

        matches = agent.match_resume_to_jds(resume_skills, jds, top_k)
        save_match(resume_id, matches)
        total_matched += 1

    return {
        "message": "All resumes matched successfully",
        "total_resumes_matched": total_matched
    }
