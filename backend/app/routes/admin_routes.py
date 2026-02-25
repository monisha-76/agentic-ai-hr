from fastapi import APIRouter, Depends, HTTPException
from app.config import database
from app.utils.jwt import get_current_user
from bson import ObjectId
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# Mongo collections
resumes_collection = database["resumes"]
jd_collection = database["job_descriptions"]
matches_collection = database["matches"]
users_collection = database["users"]


# =========================
# Admin Stats
# =========================
@router.get("/stats")
async def get_admin_stats(current_user: dict = Depends(get_current_user)):

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


# =========================
# Get Matches for a JD
# =========================
@router.get("/jd/{jd_id}/matches")
async def get_matches_for_jd(
    jd_id: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    try:
        jd_object_id = ObjectId(jd_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid JD ID")

    # Find matches containing this JD
    cursor = matches_collection.find({
        "matches.jd_id": jd_id   # stored as string inside matches array
    })

    results = []
    docs = await cursor.to_list(length=None)

    for doc in docs:
        candidate_name = doc.get("candidate_name")
        candidate_email = doc.get("candidate_email")
        resume_id = str(doc.get("resume_id"))

        for match in doc.get("matches", []):
            if str(match.get("jd_id")) == jd_id:

                results.append({
                    "resume_id": resume_id,
                    "name": candidate_name,
                    "email": candidate_email,
                    "matched_skills": match.get("matched_skills", []),
                    "extra_skills": match.get("extra_skills", []),
                    "score": round(match.get("score", 0) * 100, 2),
                    "rank": match.get("rank", 0)
                })

    # Sort by rank
    results = sorted(results, key=lambda x: x["rank"])

    return results


# =========================
# Get Candidate Profile
# =========================
@router.get("/candidate/{resume_id}")
async def get_candidate_profile(
    resume_id: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    try:
        resume = await resumes_collection.find_one({
            "_id": ObjectId(resume_id)
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid Resume ID")

    if not resume:
        raise HTTPException(status_code=404, detail="Candidate not found")

    resume["_id"] = str(resume["_id"])

    return resume


# =========================
# Send Email to Candidate
# =========================
@router.post("/send-email")
async def send_email(
    payload: dict,
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    email = payload.get("email")
    subject = payload.get("subject")
    message = payload.get("message")

    if not email or not subject or not message:
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        sender_email = "yourgmail@gmail.com"
        sender_password = "your_app_password"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # =========================
# Get JD Details
# =========================
@router.get("/jd/{jd_id}")
async def get_jd_details(
    jd_id: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    try:
        jd = await jd_collection.find_one({
            "_id": ObjectId(jd_id)
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid JD ID")

    if not jd:
        raise HTTPException(status_code=404, detail="Job not found")

    jd["_id"] = str(jd["_id"])

    return jd