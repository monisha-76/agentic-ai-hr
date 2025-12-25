from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.utils.pdf_reader import extract_text_from_pdf
from app.crud import save_resume
from app.routes import skill_routes ,jd_match_routes
from app.routes.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from app.routes.admin_routes import router as admin_router

import shutil
import os

app = FastAPI()

# ✅ ADD THIS — NO EXTRA FILE NEEDED
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
app.include_router(skill_routes.router)
app.include_router(jd_match_routes.router)

app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Agentic AI Backend is running"}


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...)
):
    # 1. Allow only PDF files
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # 2. Save uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Extract text from PDF
        text = extract_text_from_pdf(temp_file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        # 4. Save extracted text to MongoDB
        resume_id = await save_resume(name, email, text)

        return {
            "message": "Resume uploaded successfully",
            "resume_id": resume_id
        }

    finally:
        # 5. Always delete temp file (important)
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
