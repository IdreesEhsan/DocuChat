from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..services.db_service import supabase

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int
    country: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register_user(request: UserRegister):
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "name": request.name,
                    "age": request.age,
                    "country": request.country
                }
            }
        })
        if response.user:
            return {
                "message": "Registration successful. Please check your email for the OTP.",
                "user_id": response.user.id,
                "user_metadata": response.user.user_metadata
            }
        else:
            raise HTTPException(status_code=400, detail="Registration failed. User not created.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(request: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        return {
            "access_token": response.session.access_token,
            "user": response.user.user_metadata
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password.")