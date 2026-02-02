from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_db
from app.core.security import require_admin
from app.services.admin_dashboard_service import get_Admin_dashboard
from sqlalchemy.ext.asyncio import AsyncSession

router=APIRouter(prefix="/admin",tags=["admin"])

@router.get("/dashboard")
async def admin_dashboard(
    admin= Depends(require_admin),
    db: AsyncSession= Depends(get_db)
):
    return await get_Admin_dashboard(db)