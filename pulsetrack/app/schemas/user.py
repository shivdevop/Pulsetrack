from pydantic import BaseModel, EmailStr # type: ignore
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password:str

class AdminUserCreate(BaseModel):
    email: EmailStr
    password:str
    role: Literal["user","admin"]

    

class UserResponse(BaseModel):
    id:int
    email:EmailStr

    #pydantic automatically converts the orm object into json 
    class Config:
        from_attributes:True

    