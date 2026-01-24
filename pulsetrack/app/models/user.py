from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True)
    email=Column(String, nullable=False, index=True, unique=True)
    password=Column(String, nullable=False)
    role=Column(
        Enum("user","admin",name="user_roles"),
        default="user",
        nullable=False
    )
    


