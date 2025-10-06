"""
API Router for Mail Schedule endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud import mail as crud
from app.schemas import mail as schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/api/schedule/mail", # 【修改】更新 API 路徑前綴
    tags=["Mail Schedule"],      # 【修改】更新 API 文件分組標籤
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.MailSchedule, status_code=status.HTTP_201_CREATED)
def create_mail_schedule(schedule: schemas.MailScheduleCreate, db: Session = Depends(get_db)):
    """
    建立一個新的郵件發送排程。
    """
    return crud.create_schedule(db=db, schedule=schedule)

@router.get("/", response_model=List[schemas.MailSchedule])
def read_mail_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    取得郵件排程列表，支援分頁。
    """
    schedules = crud.get_schedules(db, skip=skip, limit=limit)
    return schedules

@router.get("/{id}", response_model=schemas.MailSchedule)
def read_mail_schedule(id: int, db: Session = Depends(get_db)):
    """
    根據 ID 取得單一郵件排程的詳細資訊。
    """
    db_schedule = crud.get_schedule(db, schedule_id=id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Mail Schedule not found")
    return db_schedule

@router.put("/{id}", response_model=schemas.MailSchedule) # 【修改】將 PATCH 改為 PUT
def update_mail_schedule(id: int, schedule: schemas.MailScheduleUpdate, db: Session = Depends(get_db)):
    """
    更新一個現有的郵件排程。
    """
    updated_schedule = crud.update_schedule(db=db, schedule_id=id, schedule=schedule)
    if updated_schedule is None:
        raise HTTPException(status_code=404, detail="Mail Schedule not found")
    return updated_schedule

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mail_schedule(id: int, db: Session = Depends(get_db)):
    """
    根據 ID 刪除一個郵件排程。
    """
    deleted_schedule = crud.delete_schedule(db=db, schedule_id=id)
    if deleted_schedule is None:
        raise HTTPException(status_code=404, detail="Mail Schedule not found")
    # 根據 HTTP 規範，204 回應不應該有 body，但 FastAPI 仍支援回傳方便客戶端確認
    return {"ok": True} 

# 【新增】啟用/停用任務的 API 端點
@router.patch("/{id}/status", response_model=schemas.MailSchedule)
def update_mail_schedule_status(id: int, status_update: schemas.MailScheduleStatusUpdate, db: Session = Depends(get_db)):
    """
    啟用或停用一個郵件排程。
    """
    updated_schedule = crud.update_schedule_status(db=db, schedule_id=id, is_enabled=status_update.is_enabled)
    if updated_schedule is None:
        raise HTTPException(status_code=404, detail="Mail Schedule not found")
    return updated_schedule

