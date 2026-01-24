from pwdlib import PasswordHash
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import secrets
from app.models.user import User
from app.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


password_hasher= PasswordHash.recommended()


def hash_password(password:str)->str:
    return password_hasher.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hasher.verify(plain_password, hashed_password)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)):
    try:
        payload=jwt.decode(token,settings.ACCESS_TOKEN_SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id:str = payload["sub"]
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="invalid auth credential",
                headers={"WWW-Authenticate": "Bearer"}

            )
        result=await db.execute(select(User).where(User.id==int(user_id)))
        user=result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="user not found"
            )
        
        return user 
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="invalid auth credentials",
            headers={"WWW-Authenticate": "Bearer"}

        ) 
    
def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def require_admin(user: User = Depends(get_current_user))->User:
    if user.role!="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin access required"
        )
    
    return user 