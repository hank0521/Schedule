"""資料庫操作函式 (CRUD) for Mail Schedule"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func
from app.models.mail import MailSchedule
from app.schemas.mail import MailScheduleCreate, MailScheduleUpdate, MailScheduleStatusUpdate
from typing import List, Optional
from datetime import datetime
from croniter import croniter

# --- 查詢 ---

async def get_mail_schedule(db: AsyncSession, schedule_id: int) -> Optional[MailSchedule]:
    """根據 ID 查詢單一郵件排程"""
    return await db.get(MailSchedule, schedule_id)

async def get_mail_schedules(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[MailSchedule]:
    """查詢郵件排程列表 (支援分頁)"""
    query = select(MailSchedule).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

# --- 新增 ---

async def create_mail_schedule(db: AsyncSession, schedule: MailScheduleCreate) -> MailSchedule:
    """建立新的郵件排程"""
    db_schedule = MailSchedule(**schedule.model_dump())
    if db_schedule.schedulecron:
        try:
            base_time = datetime.now()
            cron = croniter(db_schedule.schedulecron, base_time)
            db_schedule.nextexecutetime = cron.get_next(datetime)
        except ValueError:
            db_schedule.nextexecutetime = None # Or handle error appropriately
    db.add(db_schedule)
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule

# --- 更新 ---

async def update_mail_schedule(db: AsyncSession, schedule_id: int, schedule_update: MailScheduleUpdate) -> Optional[MailSchedule]:
    """更新指定的郵件排程"""
    db_schedule = await get_mail_schedule(db, schedule_id)
    if db_schedule:
        update_data = schedule_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_schedule, key, value)
        
        if 'schedulecron' in update_data:
            if db_schedule.schedulecron:
                try:
                    base_time = datetime.now()
                    cron = croniter(db_schedule.schedulecron, base_time)
                    db_schedule.nextexecutetime = cron.get_next(datetime)
                except ValueError:
                    db_schedule.nextexecutetime = None
            else:
                db_schedule.nextexecutetime = None

        db_schedule.modifieddate = func.now()
        await db.commit()
        await db.refresh(db_schedule)
    return db_schedule

async def update_mail_schedule_status(db: AsyncSession, schedule_id: int, status: str) -> Optional[MailSchedule]:
    """僅更新郵件排程的執行狀態"""
    db_schedule = await get_mail_schedule(db, schedule_id)
    if db_schedule:
        db_schedule.executionstatus = status
        if status == "Processing":
            db_schedule.lastexecutetime = func.now()
        await db.commit()
        await db.refresh(db_schedule)
    return db_schedule

async def update_mail_after_execution(db: AsyncSession, schedule_id: int, is_success: bool, error_message: Optional[str] = None):
    """在郵件發送執行後，更新其狀態、統計數據和下一次執行時間"""
    db_schedule = await get_mail_schedule(db, schedule_id)
    if not db_schedule:
        return

    if is_success:
        db_schedule.successcount += 1
        db_schedule.lastsuccesstime = func.now()
        db_schedule.lasterrormessage = None
        db_schedule.executionstatus = "Completed"
    else:
        db_schedule.failurecount += 1
        db_schedule.lasterrormessage = error_message
        db_schedule.executionstatus = "Failed"

    db_schedule.executecount += 1

    if db_schedule.schedulecron:
        try:
            base_time = datetime.now()
            cron = croniter(db_schedule.schedulecron, base_time)
            db_schedule.nextexecutetime = cron.get_next(datetime)
        except ValueError:
            db_schedule.nextexecutetime = None
    else:
        db_schedule.nextexecutetime = None # 單次任務不再執行

    await db.commit()

# --- 刪除 ---

async def delete_mail_schedule(db: AsyncSession, schedule_id: int) -> bool:
    """刪除指定的郵件排程"""
    db_schedule = await get_mail_schedule(db, schedule_id)
    if db_schedule:
        await db.delete(db_schedule)
        await db.commit()
        return True
    return False

# --- 批次處理 ---

async def get_and_lock_due_mail_schedules(db: AsyncSession, limit: int = 10) -> List[MailSchedule]:
    """
    原子性地查詢並鎖定到期的郵件任務，並將其狀態更新為 'Processing'。
    這可以有效避免高併發下的競爭條件。
    """
    # 步驟 1: 找出並鎖定符合條件的任務 ID
    # 這裡我們使用 SELECT ... FOR UPDATE SKIP LOCKED 來避免競爭
    subquery = (
        select(MailSchedule.id)
        .where(
            MailSchedule.isenabled == True,
            MailSchedule.nextexecutetime <= func.now(),
            MailSchedule.executionstatus == "Pending",
        )
        .limit(limit)
        .with_for_update(skip_locked=True)
        .subquery()
    )

    # 步驟 2: 更新被鎖定的任務，並回傳它們的完整資料
    update_query = (
        update(MailSchedule)
        .where(MailSchedule.id.in_(select(subquery)))
        .values(executionstatus="Processing", lastexecutetime=func.now())
        .returning(MailSchedule)
    )
    
    result = await db.execute(update_query)
    due_schedules = list(result.scalars().all())
    
    # 因為我們使用了 `returning`，所以需要 commit 才能讓 update 生效
    if due_schedules:
        await db.commit()
        
    return due_schedules


