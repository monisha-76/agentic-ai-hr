from app.config import resumes_collection
from datetime import datetime

async def save_resume(name: str, email: str, content: str):
    resume_doc = {
        "name": name,
        "email": email,
        "content": content,
        "uploaded_at": datetime.utcnow()
    }

    result = await resumes_collection.insert_one(resume_doc)
    return str(result.inserted_id)
