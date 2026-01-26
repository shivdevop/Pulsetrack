from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.habit import HabitCreate,HabitResponse,HabitUpdate
from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.habit import Habit
from app.models.user import User

router=APIRouter(prefix="/habits",tags=["habits"])

@router.post("",response_model=HabitResponse,status_code=201)
async def create_habit(
    data: HabitCreate,
    db: AsyncSession= Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #we have to create a new habit object basically attached with user id and persist it to db
    habit=Habit(
        user_id=current_user.id,
        name=data.name,
        frequency_type=data.frequency_type,
        target_count=data.target_count
    )

    db.add(habit)
    await db.commit()
    await db.refresh(habit)

    return habit 

@router.get("",response_model=list[HabitResponse])
async def list_habits(
    current_user: User = Depends(get_current_user),
    db: AsyncSession =Depends(get_db),
    limit: int=20,
    offset:int =0
):
    query=select(Habit).where(Habit.user_id==current_user.id).limit(limit).offset(offset)
    query_result=await db.execute(query)
    habits=query_result.scalars().all()

    return habits

