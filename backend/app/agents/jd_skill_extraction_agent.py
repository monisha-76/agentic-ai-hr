from typing import List
import os
import json
from dotenv import load_dotenv
import google.genai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client_gemini = genai.Client(api_key=GEMINI_API_KEY)


class JDSkillExtractionAgent:
    """
    Extracts technical and professional skills from
    a Job Description using Gemini LLM.
    """

    def __init__(self):
        # Use a valid model from Gemini
        self.model_name = "models/gemini-2.5-flash"

    def extract_skills(self, jd_text: str) -> List[str]:
        """
        Takes full JD text and returns a clean list of skills.
        """

        prompt = f"""
        Extract ONLY skills from the following job description.

        Rules:
        - Return ONLY a valid JSON array of strings
        - No explanation
        - No markdown
        - No numbering
        - Use short skill names

        Job Description:
        {jd_text}

        Example:
        ["Python", "React", "Node.js"]
        """

        response = client_gemini.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        raw_output = response.text.strip()

        # Safely parse JSON
        try:
            json_start = raw_output.find("[")
            json_end = raw_output.rfind("]") + 1
            skills = json.loads(raw_output[json_start:json_end])
            if isinstance(skills, list):
                return [skill.strip() for skill in skills]
        except Exception as e:
            print("Skill parsing failed:", e)

        return []