from fastapi import APIRouter 
from app.schemas.user import UserCreate

router= APIRouter(prefix="/users",tags=["users"])

@router.post("/register")
def register_user(user: UserCreate):
    return{
        "email":user.email,
        "message":"User registered successfully"
    }

