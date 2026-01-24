from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.schemas.user import UserCreate, UserResponse, AdminUserCreate
from app.models.user import User
from app.api.deps import get_db
from app.core.security import hash_password



router= APIRouter(prefix="/users",tags=["users"])

@router.post("/register",response_model=UserResponse,status_code=201)
async def register_user(user: UserCreate, db: AsyncSession=Depends(get_db)):
    
    #check if user already exists
    result=await db.execute(select(User).where(User.email==user.email))
    existing_user=result.scalar_one_or_none() #one row only, otherwise there is an error 

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    #if user not found, create a new user 
    new_user=User(
        email=user.email,
        password=hash_password(user.password)
    )

    #persist to db 
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    #return safe response 
    return new_user

@router.post("/register_admin",response_model=UserResponse,status_code=201)
async def create_user_by_admin(
    data: AdminUserCreate,
    db: AsyncSession = Depends(get_db)
):
    #check if user already exists
    result=await db.execute(select(User).where(User.email==data.email))
    existing_user=result.scalar_one_or_none() #one row only, otherwise there is an error 

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    #if user not found, create a new user 
    new_user=User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )

    #persist to db 
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    #return safe response 
    return new_user
    