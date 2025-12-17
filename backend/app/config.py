from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_USERNAME or not MONGO_PASSWORD:
    raise ValueError("MongoDB username or password not set")

MONGO_URI = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}"
    f"@{MONGO_CLUSTER}/{MONGO_DB_NAME}"
    "?retryWrites=true&w=majority"
)

client = AsyncIOMotorClient(MONGO_URI)
database = client[MONGO_DB_NAME]
resumes_collection = database["resumes"]
