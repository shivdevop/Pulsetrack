from datetime import datetime,timedelta 
from sqlalchemy import select,func
from app.models.habit_log import HabitLog
from fastapi import HTTPException

#get current window 
def get_current_window(frequency_type: str)->datetime:
    
    current_time=datetime.utcnow()

    if frequency_type=="daily":
        return current_time.replace(hour=0,minute=0,second=0,microsecond=0)
        

    if frequency_type=="weekly":
        current_window=current_time-timedelta(days=current_time.weekday())
        return current_window.replace(hour=0,minute=0,second=0,microsecond=0)
    
    return current_time.replace(hour=0,minute=0,second=0,microsecond=0)
    



#count existing logs 
async def count_existing_logs(db,habit,since):

    query=select(func.count(HabitLog.id)).where(HabitLog.habit_id==habit.id,HabitLog.completed_at>=since)
    query_result=await db.execute(query)

    return query_result.scalar_one()




#if existing logs are under target count, create new habit log and persist in db 
async def validate_and_log_habit(db,habit):

    current_window= get_current_window(habit.frequency_type)
    existing_logs_count=await count_existing_logs(db,habit,current_window)

    if existing_logs_count>=habit.target_count:
        raise HTTPException(
            status_code=400,
            detail="habit target already reached for this period"
        )
    
    log=HabitLog(
        habit_id=habit.id
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)

    return log