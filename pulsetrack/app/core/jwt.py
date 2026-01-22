from datetime import datetime, timedelta
from typing import Union
import jwt 
from app.core.config import settings


def create_access_token(data: dict, expires_delta: Union[timedelta,None]=None) -> str:
    to_encode=data.copy()

    expire=datetime.utcnow()+(expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode["exp"]=expire

    return jwt.encode(to_encode,settings.ACCESS_TOKEN_SECRET_KEY,algorithm=settings.ALGORITHM)
