from pydantic import BaseModel
from typing import Optional,Literal
from datetime import datetime 

class HabitBase(BaseModel):
    name: str
    frequency_type: Literal["daily","weekly","custom"]
    target_count: int 

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    name: Optional[str]=None
    frequency_type: Optional[Literal["daily","weekly","custom"]]=None
    target_count: Optional[int]=None 


class HabitResponse(HabitBase):
    id: int
    created_at:datetime 
    user_id: int


    class Config:
        from_attributes= True