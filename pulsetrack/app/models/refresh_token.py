from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey
from sqlalchemy.sql import func 

from app.db.base import Base

class RefreshToken(Base):
    __tablename__="refresh_tokens"

    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"),nullable=False)
    token=Column(String, nullable=False, unique=True)
    expires_at=Column(DateTime,nullable=False)
    revoked=Column(Boolean,default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    