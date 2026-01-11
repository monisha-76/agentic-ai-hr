import os
from dotenv import load_dotenv
from pymongo import MongoClient
import re
import json
from google import genai

# Load environment variables
load_dotenv()

# MongoDB Atlas credentials
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

# Construct MongoDB Atlas URI
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB_NAME}?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
resumes_collection = db["resumes"]

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client_gemini = genai.Client(api_key=GEMINI_API_KEY)


def clean_text(text):
    """Clean and normalize resume text."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9,.\s]', '', text)
    return text.strip()


def extract_skills_with_llm(resume_text):
    """Use Gemini LLM to extract skills. Returns a Python list."""
    prompt = f"""
    Extract all technical skills, programming languages, frameworks, and tools
    from the resume text below.

    Return ONLY a valid JSON array of strings.
    Do NOT add explanations or extra text.

    Resume Text:
    {resume_text}

    Example:
    ["Python", "React", "Node.js"]
    """

    response = client_gemini.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    raw_text = response.text.strip()

    # Safely extract JSON array
    try:
        json_start = raw_text.find("[")
        json_end = raw_text.rfind("]") + 1
        skills = json.loads(raw_text[json_start:json_end])
        if not isinstance(skills, list):
            skills = []
    except Exception as e:
        print("Skill parsing failed:", e)
        skills = []

    return skills


def extract_experience_with_llm(resume_text):
    """
    Use Gemini LLM to extract experience from resume text.
    Returns a structured dictionary:
    {
        "total_years": float,
        "roles": [
            {"title": "Software Engineer", "company": "XYZ", "duration": "2 years"},
            ...
        ]
    }
    If no experience is found, returns defaults.
    """
    prompt = f"""
    Extract the professional experience from the resume text below.
    Return a JSON object with the following format:

    {{
        "total_years": <number of years of experience, 0 if none>,
        "roles": [
            {{
                "title": "<job title>",
                "company": "<company name>",
                "duration": "<duration>"
            }}
        ]
    }}

    If no experience is mentioned, return total_years as 0 and roles as an empty list.

    Resume Text:
    {resume_text}
    """

    response = client_gemini.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    raw_text = response.text.strip()

    # Safely extract JSON object
    try:
        json_start = raw_text.find("{")
        json_end = raw_text.rfind("}") + 1
        experience = json.loads(raw_text[json_start:json_end])
        if not isinstance(experience, dict):
            experience = {"total_years": 0, "roles": []}
    except Exception as e:
        print("Experience parsing failed:", e)
        experience = {"total_years": 0, "roles": []}

    return experience


def process_resume(resume_id):
    """Process a single resume by MongoDB _id."""
    resume = resumes_collection.find_one({"_id": resume_id})

    if not resume or "content" not in resume:
        print(f"Resume {resume_id} not found or has no content.")
        return

    cleaned_text = clean_text(resume["content"])
    skills = extract_skills_with_llm(cleaned_text)
    experience = extract_experience_with_llm(cleaned_text)

    resumes_collection.update_one(
        {"_id": resume_id},
        {"$set": {"skills": skills, "experience": experience}}
    )

    print(f"Skills and experience updated for resume {resume_id}")


def process_all_resumes():
    """Process all resumes."""
    for resume in resumes_collection.find():
        process_resume(resume["_id"])


if __name__ == "__main__":
    process_all_resumes()