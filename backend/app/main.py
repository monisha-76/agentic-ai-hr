from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime
import shutil
import os

from app.utils.pdf_reader import extract_text_from_pdf
from app.crud import save_resume, resumes_collection
from app.skill_extraction_agent import process_resume
from app.config import database
from app.utils.jwt import get_current_user
from app.agents.jd_matching_agent import JDMatchingAgent

# Import all routers
from app.routes.auth_routes import router as auth_router
from app.routes.admin_routes import router as admin_router
from app.routes.candidate_routes import router as candidate_router
from app.routes.skill_routes import router as skill_router
from app.routes.jd_match_routes import router as jd_match_router

app = FastAPI(title="Agentic AI Backend")

# -------------------
# CORS
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Routers
# -------------------
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(candidate_router)
app.include_router(skill_router)
app.include_router(jd_match_router)



users_collection = database["users"]
# -------------------
# Database collections
# -------------------
matches_collection = database["matches"]

# -------------------
# JD Matching Agent
# -------------------
match_agent = JDMatchingAgent()

# -------------------
# Root
# -------------------
@app.get("/")
def root():
    return {"message": "Agentic AI Backend is running"}

# -------------------
# Upload Resume Endpoint
# -------------------
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    jd_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    # Only candidate can upload
    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    temp_file_path = f"temp_{file.filename}"

    try:
        # Save PDF temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        text = extract_text_from_pdf(temp_file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume")

        # Save resume to MongoDB
        resume_id = await save_resume(
            name=name,
            email=email,
            content=text,
            jd_id=jd_id,
            candidate_id=current_user["id"]
        )

        # Extract skills & experience (synchronous)
        process_resume(ObjectId(resume_id))

        # Fetch resume after extraction
        resume_doc = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
        resume_skills = resume_doc.get("skills", [])

        # Fetch JD
        jd_doc = await database["job_descriptions"].find_one({"_id": ObjectId(jd_id)})

        if jd_doc and resume_skills:
            match_result = match_agent.match_resume_to_jds(resume_skills, [jd_doc], top_k=1)[0]

            # Extra skills
            extra_skills = list(set(resume_skills) - set(match_result["matched_skills"]))
            match_result["extra_skills"] = extra_skills

            # Save match
            match_doc = {
                "resume_id": ObjectId(resume_id),
                "candidate_name": name,
                "candidate_email": email,
                "matches": [match_result],
                "created_at": datetime.utcnow()
            }
            matches_collection.insert_one(match_doc)

        return {
            "message": "Resume uploaded, skills extracted & matched with JD!",
            "resume_id": resume_id
        }

    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
