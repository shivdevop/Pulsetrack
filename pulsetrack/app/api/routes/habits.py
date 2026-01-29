from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.habit import HabitCreate,HabitResponse,HabitUpdate
from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.habit import Habit
from app.models.user import User
from app.services.health_log import validate_and_log_habit

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



#get single habit details
@router.get("/{habit_id}",response_model=HabitResponse)
async def get_habit(
    habit_id: int,
    current_user:User =Depends(get_current_user),
    db: AsyncSession=Depends(get_db)
):
    query=select(Habit).where(Habit.id==habit_id,Habit.user_id==current_user.id)
    query_result=await db.execute(query)
    habit=query_result.scalar_one_or_none()

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="habit not found"
        )
    
    return habit 


#update a particular habit
@router.patch("/{habit_id}",response_model=HabitResponse)
async def update_habit(
    habit_id:int,
    update_data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    query=select(Habit).where(Habit.id==habit_id,Habit.user_id==current_user.id)
    query_result=await db.execute(query)

    habit=query_result.scalar_one_or_none()
    if not habit:
        raise HTTPException(
            status_code=404,
            detail="habit not found"
        )
    
    for field,value in update_data.dict(exclude_unset=True).items():
        setattr(habit,field,value)

    await db.commit()
    await db.refresh(habit)

    return habit 





#delete a particular habit 
@router.delete("/{habit_id}",status_code=204)
async def delete_habit(
    habit_id: int,
    current_user:User =Depends(get_current_user),
    db: AsyncSession=Depends(get_db)
):
    query=select(Habit).where(Habit.id==habit_id,Habit.user_id==current_user.id)
    query_result=await db.execute(query)
    habit=query_result.scalar_one_or_none()

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="habit not found"
        )
    
    await db.delete(habit)
    await db.commit()
    


#log a habit completion for a particular user for a particular habit 
#so first user needs to be authenticated
#then we need to find the habit with respect to the id provided
#then we need to check if the habit log is allowed 
#we will count the habit logs in the current period and if its greater than or equal to target count->
#->it means that the target is already achieved and we cant log more !!
#if target_count not already achieved then we will log the habit !!!!
@router.post("/{habit_id}/log",status_code=201)
async def log_habit(
    habit_id: int,
    user: User =Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    #first get the habit from db 
    query=select(Habit).where(Habit.id==habit_id,Habit.user_id==user.id)
    query_result=await db.execute(query)
    habit=query_result.scalar_one_or_none()

    if not habit:
        raise HTTPException(
            status_code=404,
            detail="habit not found"
        )
    
    log=await validate_and_log_habit(db,habit)

    return {
        "message":"Habit logged successfully",
        "logged_at":log.completed_at
    }




