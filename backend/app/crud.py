from app.config import resumes_collection
from datetime import datetime

async def save_resume(
    name,
    email,
    content,
    jd_id,
    candidate_id
):
    resume = {
        "name": name,
        "email": email,
        "content": content,
        "jd_id": jd_id,
        "candidate_id": candidate_id,
        "created_at": datetime.utcnow()
    }

    result = await resumes_collection.insert_one(resume)
    return str(result.inserted_id)
