from sqlalchemy import Column,ForeignKey,Integer,DateTime 
from datetime import datetime 
from sqlalchemy.orm import relationship 
from app.db.base import Base 

class HabitLog(Base):
    __tablename__="habit_logs"

    id=Column(Integer,primary_key=True)
    habit_id=Column(Integer,ForeignKey("habits.id",ondelete="CASCADE"),nullable=False)
    completed_at=Column(DateTime,default=datetime.utcnow(),nullable=False)
    #we store habit log when habit was done 
    habit=relationship("Habit",back_populates="logs")
    
