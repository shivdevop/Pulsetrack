from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.user import User
from app.models.habit import Habit
from app.models.refresh_token import RefreshToken
from app.models.habit_log import HabitLog

#get total users
async def get_total_users(db:AsyncSession)-> int:

    result=await db.execute(select(func.count(User.id)))
    return result.scalar_one()

#get active users 
async def get_active_users(db:AsyncSession)->int:

    result= await db.execute(select(func.count(func.distinct(RefreshToken.user_id))).where(RefreshToken.revoked==False))

    return result.scalar_one()



#get most popular habits 
#current implementation -- which habit name was logged the most !!!
async def get_most_popular_habits(db: AsyncSession, limit: int = 5):

    result=await db.execute(
        select(Habit.name, func.count(HabitLog.id).label("log_count")).
        join(HabitLog, HabitLog.habit_id==Habit.id).
        group_by(Habit.name).
        order_by(func.count(HabitLog.id).desc()).limit(limit)
    )

    return result.all()

async def get_Admin_dashboard(db: AsyncSession):
    return{
        "total users": await get_total_users(db),
        "active users": await get_active_users(db),
        "popular_habits":[
            {
                "name":habit.name,
                "completed":habit.log_count
            }
            for habit in await get_most_popular_habits(db)
        ]
    }