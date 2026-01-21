from pydantic import BaseModel, EmailStr # type: ignore

class UserCreate(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr

    #pydantic automatically converts the orm object into json 
    class Config:
        from_attributes:True

    