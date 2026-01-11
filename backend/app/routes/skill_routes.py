from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.skill_extraction_agent import process_resume, process_all_resumes

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

@router.post("/extract/{resume_id}")
def extract_skills_for_resume(resume_id: str):
    """
    Extract skills for a single resume by ID.
    """
    try:
        process_resume(ObjectId(resume_id))
        return {"message": f"Skills extracted for resume {resume_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract_all")
def extract_skills_for_all():
    """
    Extract skills for all resumes in the database.
    """
    try:
        process_all_resumes()
        return {"message": "Skills extracted for all resumes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))