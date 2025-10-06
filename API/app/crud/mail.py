"""
CRUD (Create, Read, Update, Delete) operations for Mail Schedules.
"""
from sqlalchemy.orm import Session
from app.models import mail as models
from app.schemas import mail as schemas
from datetime import datetime

def get_schedule(db: Session, schedule_id: int):
    """根據 ID 取得單一郵件排程"""
    return db.query(models.MailSchedule).filter(models.MailSchedule.id == schedule_id).first()

def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    """取得郵件排程列表 (分頁)"""
    return db.query(models.MailSchedule).offset(skip).limit(limit).all()

def create_schedule(db: Session, schedule: schemas.MailScheduleCreate):
    """建立新的郵件排程"""
    db_schedule = models.MailSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def update_schedule(db: Session, schedule_id: int, schedule: schemas.MailScheduleUpdate):
    """更新現有的郵件排程"""
    db_schedule = get_schedule(db, schedule_id)
    if not db_schedule:
        return None
    
    update_data = schedule.dict(exclude_unset=True)
    update_data['modifieddate'] = datetime.utcnow() # 手動更新修改時間

    for key, value in update_data.items():
        setattr(db_schedule, key, value)
        
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def delete_schedule(db: Session, schedule_id: int):
    """刪除郵件排程"""
    db_schedule = get_schedule(db, schedule_id)
    if not db_schedule:
        return None
    db.delete(db_schedule)
    db.commit()
    return db_schedule

# 【新增】更新郵件排程的啟用狀態
def update_schedule_status(db: Session, schedule_id: int, is_enabled: bool):
    """更新郵件排程的啟用狀態"""
    db_schedule = get_schedule(db, schedule_id)
    if not db_schedule:
        return None
    
    db_schedule.isenabled = is_enabled
    db_schedule.modifieddate = datetime.utcnow() # 手動更新修改時間
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

