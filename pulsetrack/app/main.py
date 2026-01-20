from fastapi import FastAPI # type: ignore
from app.api.routes.users import router as user_router 
from app.db.session import engine
from app.db.base import Base
from app.models.user import User


app=FastAPI()

@app.get("/health")
def health_check():
    return {"status":"ok"}


app.include_router(user_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)