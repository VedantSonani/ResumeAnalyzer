from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.core.auth import create_access_token
from app.models import UserSignup

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(credentials: LoginRequest):
    # verify login credentials, will do it later
    # For now, just create token

    jwt_token = create_access_token(credentials.email)

    return {
        "msg": "Login successful!",
        "token": jwt_token
    }

@router.post("/signup")
async def sign_up(user_info: UserSignup):
    # add user_info into db, hash password

    # redirect to login page
    return {
        "msg": "Sign up successful! You can now log in."
    }

@router.post("/logout")
async def logout():
    return {
        "message": "Logged out successfully. Please delete your token."
    }
