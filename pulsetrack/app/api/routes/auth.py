from datetime import timedelta 

from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

from app.api.deps import get_db
from app.core.jwt import create_access_token
from app.core.security import verify_password,get_current_user
from app.core.config import settings
from app.models.user import User

router=APIRouter(tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm =Depends(),
                db: AsyncSession =Depends(get_db)):
    
    #verify if the user exist or not 
    result=await db.execute(select(User).where(User.email==form_data.username))
    user=result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    #if user is present, then verify the password 
    if not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #create jwt token now 
        # 3) Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


    
    
@router.get("/me")
def get_current_user(current_user:int =Depends(get_current_user)):
    return {"message":f"hello current user {current_user}"}