from pwdlib import PasswordHash
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import secrets


password_hasher= PasswordHash.recommended()


def hash_password(password:str)->str:
    return password_hasher.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hasher.verify(plain_password, hashed_password)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,settings.ACCESS_TOKEN_SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id:str = payload["sub"]
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="invalid auth credential",
                headers={"WWW-Authenticate": "Bearer"}

            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="invalid auth credentials",
            headers={"WWW-Authenticate": "Bearer"}

        ) 
    
def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)