from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.user import User


from app.services.dashboard_services import get_dashboard_overview,get_dashboard_habits


router=APIRouter(prefix="/dashboard",tags=["dashboard"])

@router.get("/overview")
async def dashboard_overview(
    db:AsyncSession=Depends(get_db),
    user:User = Depends(get_current_user)
):
    return await get_dashboard_overview(db,user)



@router.get("/habits")
async def dashboard_habits(
    db:AsyncSession=Depends(get_db),
    user:User = Depends(get_current_user)
):
    return await get_dashboard_habits(db,user)