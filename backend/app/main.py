from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import shutil
import os

from app.utils.pdf_reader import extract_text_from_pdf
from app.crud import save_resume
from app.skill_extraction_agent import process_resume

from app.routes import skill_routes, jd_match_routes
from app.routes.auth_routes import router as auth_router
from app.routes.admin_routes import router as admin_router
from app.routes.candidate_routes import router as candidate_router

from app.config import database
from app.utils.jwt import get_current_user

app = FastAPI()

# ✅ CORS
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

# Routers
app.include_router(skill_routes.router)
app.include_router(jd_match_routes.router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(candidate_router)


@app.get("/")
def root():
    return {"message": "Agentic AI Backend is running"}


users_collection = database["users"]


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    jd_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    # 🔐 Candidate only
    if current_user.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Candidate access only")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(temp_file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text")

        # ✅ Save resume (manual name + email)
        resume_id = await save_resume(
            name=name,
            email=email,
            content=text,
            jd_id=jd_id,
            candidate_id=current_user["id"]  # from JWT
        )

        # 🔥 Auto skill + experience extraction
        process_resume(ObjectId(resume_id))

        return {
            "message": "Resume uploaded & skills extracted",
            "resume_id": resume_id
        }

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
