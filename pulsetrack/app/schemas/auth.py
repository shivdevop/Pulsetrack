from pydantic import BaseModel 
from datetime import datetime 

class RefreshTokenRequest(BaseModel):
    refresh_token: str 

class LogoutRequest(BaseModel):
    refresh_token: str 

class SessionResponse(BaseModel):
    id: int
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes=True
