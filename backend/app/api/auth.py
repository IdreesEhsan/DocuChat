from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from ..core.supabase import supabase
from ..core.auth import get_password_hash, verify_password, create_access_token, get_current_user
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenResponse)
async def register(user: UserRegister):
    existing = supabase.table("users").select("id").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed = get_password_hash(user.password)
    new_user = {
        "id": str(uuid.uuid4()),
        "email": user.email,
        "password_hash": hashed,
    }
    result = supabase.table("users").insert(new_user).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Registration failed")

    token = create_access_token({"sub": new_user["id"], "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("login", response_model=TokenResponse)
async def login(user: UserLogin):
    result = supabase.table("users").select("*").eq("email", user.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    db_user = result.data[0]
    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": db_user["id"], "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    result = supabase.table("users").select("id, email").eq("id", current_user["id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    return result.data[0]