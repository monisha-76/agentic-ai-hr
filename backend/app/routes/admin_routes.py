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
profiles_collection = database["profiles"]   # ✅ added


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
        ObjectId(jd_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid JD ID")

    cursor = matches_collection.find({
        "matches.jd_id": jd_id
    })

    results = []
    docs = await cursor.to_list(length=None)

    for doc in docs:
        candidate_name = doc.get("candidate_name")
        candidate_email = doc.get("candidate_email")
        resume_id = str(doc.get("resume_id"))

        # ✅ candidate_id from resume document
        resume_doc = await resumes_collection.find_one(
            {"_id": ObjectId(resume_id)}
        )

        candidate_id = None
        if resume_doc:
            candidate_id = resume_doc.get("candidate_id")

        for match in doc.get("matches", []):
            if str(match.get("jd_id")) == jd_id:

                results.append({
                    "candidate_id": candidate_id,   # ✅ NEW FIELD
                    "resume_id": resume_id,
                    "name": candidate_name,
                    "email": candidate_email,
                    "matched_skills": match.get("matched_skills", []),
                    "extra_skills": match.get("extra_skills", []),
                    "score": round(match.get("score", 0) * 100, 2),
                    "rank": match.get("rank", 0)
                })

    results = sorted(results, key=lambda x: x["rank"])

    return results


# =========================
# Get Candidate Profile (using candidate_id)
# =========================
@router.get("/candidate/{candidate_id}")
async def get_candidate_profile(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    profile = await profiles_collection.find_one({
        "candidate_id": candidate_id
    })

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile["_id"] = str(profile["_id"])

    return profile

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
    name = payload.get("name")
    job_title = payload.get("job_title", "the position")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email")

    try:
        sender_email = "monishamoorthy.16@gmail.com"
        sender_password = "xchzsbixtekhtobv"

        subject = f"Shortlisted for Next Round – {job_title}"

        message = f"""
Dear {name},

Congratulations!

We are pleased to inform you that you have been shortlisted for the role of {job_title} based on your profile evaluation.

Our recruitment process includes the following rounds:

• DSA and Aptitute 
• Technical Interview
• Managerial Discussion
• HR Round

Our recruitment team will contact you shortly with further details.

Best regards,
Recruitment Team
"""

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
        print("EMAIL ERROR:", e) 
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