from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.services.health_log import calculate_streak



async def get_total_habits(db: AsyncSession, user: User)-> int:
    query=select(func.count(Habit.id)).where(Habit.user_id==user.id)
    queryresult=await db.execute(query)

    return queryresult.scalar_one()


#we want to check how many habits have met their target today 
#so we have to get today's logs, group them by habits and then compare count vs target 

async def habits_completed_today(db:AsyncSession, user:User)->int:

    today_start=datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
    today_end=today_start+timedelta(days=1)

    result=await db.execute(
        select(Habit.id).join(HabitLog).where(
            Habit.user_id==user.id,
            HabitLog.completed_at>=today_start,
            HabitLog.completed_at<today_end
        ).group_by(Habit.id).having(func.count(HabitLog.id)==Habit.target_count)
    )

    return len(result.all())


#get active streaks. basically check how many habits are having active streaks

async def get_active_streaks(db:AsyncSession, user: User)->int:
    #find all habits of user first

    result=await db.execute(select(Habit).where(Habit.user_id==User.id))
    habits=result.scalars().all()

    active_Streaks=0
    for habit in habits:
        streak= await calculate_streak(db,habit)
        if streak>0:
            active_Streaks+=1

    return active_Streaks

        