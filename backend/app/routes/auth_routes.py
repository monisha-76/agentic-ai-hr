from fastapi import APIRouter, HTTPException
from app.config import users_collection   # 👈 IMPORTANT
from app.models.user_model import SignupModel, LoginModel
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "123456"

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ✅ SIGNUP – CANDIDATES ONLY
@router.post("/signup")
async def signup(user: SignupModel):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": "candidate"
    }

    await users_collection.insert_one(new_user)
    return {"message": "Candidate registered successfully"}


# ✅ LOGIN – ADMIN OR CANDIDATE
@router.post("/login")
async def login(credentials: LoginModel):

    # 🔐 ADMIN LOGIN (HARDCODED)
    if (
        credentials.email == ADMIN_EMAIL
        and credentials.password == ADMIN_PASSWORD
    ):
        token = create_access_token({
            "id":"admin",
            "email": credentials.email,
            "role": "admin"
        })

        return {
            "message": "Admin login successful",
            "role": "admin",
            "token": token
        }

    # 👤 CANDIDATE LOGIN
    user = await users_collection.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "id": str(user["_id"]),
        "email": user["email"],
        "role": "candidate"
    })

    return {
        "message": "Candidate login successful",
        "role": "candidate",
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }