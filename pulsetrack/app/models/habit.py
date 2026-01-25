from sqlalchemy import Column, Integer, String, ForeignKey, Enum 
from sqlalchemy.orm  import relationship 
from app.db.base import Base 

class Habit(Base):
    __tablename__="habits"

    id=Column(Integer, primary_key=True)
    user_id=Column(
        Integer, ForeignKey("users.id",ondelete="CASCADE"),nullabe=False
    )

    name=Column(String, nullable=False)
    frequency_type=Column(
        Enum("daily","weekly","custom",name="habit_frequency"),
        nullable=False
    )
    target_count=Column(Integer, nullable=False)
    user=relationship("User",back_populates="habits")
    