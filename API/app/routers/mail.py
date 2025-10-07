"""
郵件排程任務的 CRUD API 路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import mail as schemas_mail
from app.crud import mail as crud_mail

router = APIRouter(
    prefix="/api/schedule/mail",
    tags=["Mail Schedule"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas_mail.MailSchedule, status_code=status.HTTP_201_CREATED, summary="建立新的郵件排程任務")
async def create_mail_schedule(schedule: schemas_mail.MailScheduleCreate, db: Session = Depends(get_db)):
    """
    建立一個新的郵件排程任務。

    - **progcode**: 程式代碼，用於識別任務來源。
    - **subject**: 郵件主旨。
    - **body**: 郵件內容 (HTML 或 TEXT)。
    - **sender**: 寄件者 Email。
    - **recipients**: 收件者 Email (多個請用分號 `;` 分隔)。
    - **schedulecron**: 選填，用於設定週期性任務的 CRON 表達式。
    """
    return await crud_mail.create_mail_schedule(db=db, schedule=schedule)


@router.get("/", response_model=List[schemas_mail.MailSchedule], summary="查詢郵件排程任務列表")
async def read_mail_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    讀取郵件排程任務的列表，支援分頁。
    """
    schedules = await crud_mail.get_mail_schedules(db, skip=skip, limit=limit)
    return schedules


@router.get("/{id}", response_model=schemas_mail.MailSchedule, summary="查詢單一郵件排程任務")
async def read_mail_schedule(id: int, db: Session = Depends(get_db)):
    """
    根據 ID 讀取單一郵件排程任務的詳細資訊。
    """
    db_schedule = await crud_mail.get_mail_schedule(db, schedule_id=id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="找不到指定的郵件排程任務")
    return db_schedule


@router.put("/{id}", response_model=schemas_mail.MailSchedule, summary="更新郵件排程任務")
async def update_mail_schedule(id: int, schedule: schemas_mail.MailScheduleUpdate, db: Session = Depends(get_db)):
    """
    根據 ID 更新一個已存在的郵件排程任務。
    """
    db_schedule = await crud_mail.update_mail_schedule(db=db, schedule_id=id, schedule_update=schedule)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="找不到指定的郵件排程任務")
    return db_schedule


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="刪除郵件排程任務")
async def delete_mail_schedule(id: int, db: Session = Depends(get_db)):
    """
    根據 ID 刪除一個郵件排程任務。
    """
    success = await crud_mail.delete_mail_schedule(db=db, schedule_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="找不到指定的郵件排程任務")
    return


@router.patch("/{id}/status", response_model=schemas_mail.MailSchedule, summary="啟用或停用郵件排程任務")
async def update_mail_schedule_status(id: int, status_update: schemas_mail.MailScheduleStatusUpdate, db: Session = Depends(get_db)):
    """
    根據 ID 更新一個郵件排程任務的啟用狀態 (`isenabled`)。
    """
    db_schedule = await crud_mail.update_mail_schedule_status(db=db, schedule_id=id, is_enabled=status_update.isenabled)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="找不到指定的郵件排程任務")
    return db_schedule

