from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Optional[dict] = None
