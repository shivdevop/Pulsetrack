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


def get_start_time_for_date(date:datetime,frequency_type):

    if frequency_type == "daily":
        return date.replace(hour=0, minute=0, second=0, microsecond=0)

    if frequency_type == "weekly":
        start = date - timedelta(days=date.weekday())
        return start.replace(hour=0, minute=0, second=0, microsecond=0)

    return date.replace(hour=0, minute=0, second=0, microsecond=0)

    #custom frequency type implementation later         


async def did_habit_succeed(startTime,endTime,db,habit)->bool:

    #we need to count the number of logs for the habit id within start time and end time 
    query=select(func.count(HabitLog.id)).where(
        HabitLog.habit_id==habit.id,HabitLog.completed_at>=startTime,HabitLog.completed_at<endTime)
    queryresult=await db.execute(query)
    count=queryresult.scalar_one()
    
    return count==habit.target_count 



async def calculate_streak(db,habit):

    now=datetime.utcnow()
    if habit.frequency_type=="daily":
        cursor=now - timedelta(days=1)
    elif habit.frequency_type=="weekly":
        cursor=now - timedelta(weeks=1)

    #custom frequency_type habit implementation later     
    streak=0

    for _ in range(365):
        #so basically we are trying to find out startime and endtime for every day or week going backwards and try to see if the habit target was achieved. if so we increase our streak else we break and return the computed streak till that point 

        startTime=get_start_time_for_date(cursor,habit.frequency_type)

        if habit.frequency_type=="daily":
            endTime=startTime+timedelta(days=1)
            cursor-=timedelta(days=1)
        
        else:
            endTime=startTime+timedelta(weeks=1)
            cursor-=timedelta(weeks=1)

        #for custom frequency_type we will do the implementation later 

        success=await did_habit_succeed(startTime,endTime,db,habit)

        if not success:
            break

        streak+=1

    return streak        



    