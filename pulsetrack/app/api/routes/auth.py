from datetime import datetime, timedelta

from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update 

from app.api.deps import get_db
from app.core.jwt import create_access_token
from app.core.security import verify_password,get_current_user,create_refresh_token
from app.core.config import settings
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth import RefreshTokenRequest,LogoutRequest,SessionResponse

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

    refresh_token=create_refresh_token()
    refresh_token_expires_at=datetime.utcnow()+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_obj=RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=refresh_token_expires_at
    )

    db.add(refresh_token_obj)
    await db.commit()



    return {"access_token": access_token,"refresh_token":refresh_token, "token_type": "bearer"}


    
    
@router.get("/me")
def current_user(current_user:int =Depends(get_current_user)):
    return {"message":f"hello current user {current_user}"}

@router.post("/refresh")
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):

    #find refresh token in db 
    result=await db.execute(select(RefreshToken).where(RefreshToken.token==data.refresh_token))
    refresh_token=result.scalar_one_or_none()

    if(not refresh_token or refresh_token.revoked==True or refresh_token.expires_at<datetime.utcnow()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired refresh token"
        )
    
    #refresh token is valid, so now find the user with this token's user id 
    user_result= await db.execute(select(User).where(User.id==refresh_token.user_id))
    user=user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status=status.HTTP_401_UNAUTHORIZED,
            detail="couldn't find user"
        )
    
    #since user is found, we will revoke old refresh token, issue a new refresh token and persist to db 

    refresh_token.revoked=True
    new_refresh_token=create_refresh_token()

    new_refresh_token_obj=RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=datetime.utcnow()+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(new_refresh_token_obj)

    #create new access access token
    access_token_toencode_data={
        "sub":str(user.id)
    }

    new_access_token=create_access_token(access_token_toencode_data)

    #persist new refresh token in db 
    await db.commit()

    #return new tokens 
    return{
        "access_token":new_access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer"
    }

@router.post("/logout")
async def logout(data: LogoutRequest, db: AsyncSession = Depends(get_db)):

    #Find Refresh Token 
    result=await db.execute(select(RefreshToken).where(RefreshToken.token==data.refresh_token))
    refresh_token=result.scalar_one_or_none()
    
    #if refresh token already invalidated, then logout!!!
    if not refresh_token or refresh_token.revoked:
        return {"message":"logged out successfully"}
    
    #revoke refresh token 
    await db.execute(update(RefreshToken).where(RefreshToken.id==refresh_token.id).values(revoked=True))

    await db.commit()

    return{
        "message":"Logged out successfully"
    }

@router.get("/activeSessions",response_model=list[SessionResponse])
async def list_sessions(current_user_id:int =Depends(get_current_user),
                        db: AsyncSession= Depends(get_db)):
    result=await db.execute(select(RefreshToken).where(
        RefreshToken.user_id==current_user_id,
        RefreshToken.revoked==False
    ).order_by(RefreshToken.created_at.desc()))

    sessions=result.scalars().all()
    return sessions
