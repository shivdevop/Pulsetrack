from fastapi import FastAPI # type: ignore
from app.api.routes.users import router as user_router 
from app.api.routes.auth import router as auth_router 
from app.api.routes.habits import router as habits_router
from app.api.routes.dashboards import router as dashboard_router
from app.api.routes.admin_dashboard import router as admin_router
from app.db.session import engine
from app.db.base import Base
from app.models.user import User


app=FastAPI()

@app.get("/health")
def health_check():
    return {"status":"ok"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(habits_router)
app.include_router(dashboard_router)
app.include_router(admin_router)