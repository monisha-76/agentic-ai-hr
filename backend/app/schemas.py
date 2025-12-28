from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ResumeCreate(BaseModel):
    name: str
    email: EmailStr
    content: str
    jd_id: str


class ResumeResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    uploaded_at: datetime
