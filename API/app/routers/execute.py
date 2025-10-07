"""
手動執行 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# 修正：導入 db_manager 來為背景任務建立新的資料庫連線
from app.core.database import get_db, db_manager
from app.crud import mail as crud_mail
from app.services import email_sender
from app.schemas import mail as schemas_mail

router = APIRouter(
    prefix="/api/execute",
    tags=["Execution"],
    responses={404: {"description": "Not found"}},
)


@router.post("/mail/trigger-due", status_code=202, summary="觸發處理所有到期的郵件任務")
async def trigger_due_mail_schedules(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    根據排程規則，查詢並觸發所有到期的郵件任務。

    - **原子性操作**：查詢並立即將任務狀態更新為 "Processing"，避免高併發下的重複處理。
    - **背景處理**：實際的郵件發送會在背景執行，API 會立即返回，不會讓使用者等待。
    """
    due_schedules = await crud_mail.get_and_lock_due_mail_schedules(db)
    count = len(due_schedules)

    if count > 0:
        for schedule in due_schedules:
            background_tasks.add_task(process_and_send_mail, schedule_id=schedule.id)

    return {"message": f"已接收請求，正在背景處理 {count} 個郵件任務。"}


@router.post("/mail/{id}", status_code=202, summary="手動觸發單一郵件任務")
async def trigger_single_mail_schedule(
    id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    根據提供的 ID，立即執行一個特定的郵件排程任務。
    """
    db_schedule = await crud_mail.get_mail_schedule(db=db, schedule_id=id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="找不到指定的郵件排程任務")

    background_tasks.add_task(process_and_send_mail, schedule_id=id)

    return {"message": f"已接收請求，正在背景處理郵件任務 ID: {id}"}


async def process_and_send_mail(schedule_id: int):
    """
    一個共用的背景函式，用於處理並發送單一郵件。
    此函式會建立自己的資料庫 session，以確保在背景安全執行。
    """
    # 修正：使用 db_manager.get_session() 來建立全新的、獨立的資料庫連線
    async with db_manager.get_session() as db:
        schedule = await crud_mail.get_mail_schedule(db=db, schedule_id=schedule_id)
        if not schedule:
            return

        await crud_mail.update_mail_schedule_status(db, schedule_id, "Processing")

        is_success, message = await email_sender.send_schedule_mail(schedule)

        await crud_mail.update_mail_after_execution(
            db=db,
            schedule_id=schedule_id,
            is_success=is_success,
            error_message=None if is_success else message
        )






