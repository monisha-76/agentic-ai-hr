import os
from dotenv import load_dotenv
from google import genai

# Load .env variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
print("Available Gemini Models:\n")

for model in client.models.list():
    print(model.name)
