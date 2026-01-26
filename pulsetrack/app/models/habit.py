from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm  import relationship 
from app.db.base import Base 
from app.models.habit_log import HabitLog
from sqlalchemy.sql import func


class Habit(Base):
    __tablename__="habits"

    id=Column(Integer, primary_key=True)
    user_id=Column(
        Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False
    )

    name=Column(String, nullable=False)
    frequency_type=Column(
        Enum("daily","weekly","custom",name="habit_frequency"),
        nullable=False
    )
    created_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    target_count=Column(Integer, nullable=False)
    user=relationship("User",back_populates="habits")
    logs=relationship("HabitLog",back_populates="habit",cascade="all,delete-orphan")
