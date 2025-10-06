"""
Pydantic Schemas for Mail Schedule data validation.

MailScheduleCreate: 建立新任務時，前端需要傳送的資料格式。

MailScheduleUpdate: 更新任務時，前端可以傳送的資料格式。

MailSchedule: API 回傳任務資料給前端時的完整格式。

MailScheduleStatusUpdate: 更新任務啟用狀態時的專用格式。
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 基礎模型，包含所有 Mail Schedule 共用的欄位
class MailScheduleBase(BaseModel):
    progcode: str = Field(..., max_length=200, description="程式代碼")
    sender: str = Field(..., max_length=200, description="寄件者信箱")
    sendername: Optional[str] = Field(None, max_length=200, description="寄件者名稱")
    recipients: str = Field(..., description="收件者 (多個以分號分隔)")
    cc: Optional[str] = Field(None, description="副本收件者 (多個以分號分隔)")
    bcc: Optional[str] = Field(None, description="密件副本收件者 (多個以分號分隔)")
    replyto: Optional[str] = Field(None, max_length=200, description="回覆信箱")
    subject: str = Field(..., max_length=500, description="郵件主旨")
    body: str = Field(..., description="郵件內容")
    bodytype: str = Field("HTML", description="郵件格式 (HTML/TEXT)")
    priority: str = Field("Normal", description="優先順序 (Low/Normal/High)")
    encoding: str = Field("UTF-8", max_length=50, description="編碼")
    attachmentpaths: Optional[str] = Field(None, description="附件路徑 (多個以分號分隔)")
    smtphost: Optional[str] = Field(None, max_length=200)
    smtpport: Optional[int] = 587
    smtpusername: Optional[str] = Field(None, max_length=200)
    smtppassword: Optional[str] = Field(None, max_length=500)
    smtpenablessl: Optional[bool] = True
    smtptimeoutseconds: Optional[int] = 30
    isenabled: Optional[bool] = True
    schedulecron: Optional[str] = Field(None, max_length=100, description="排程 CRON 表達式")
    createdby: Optional[str] = Field(None, max_length=100)
    modifiedby: Optional[str] = Field(None, max_length=100)
    remark: Optional[str] = None

# 用於「建立」新排程的模型 (繼承基礎模型)
class MailScheduleCreate(MailScheduleBase):
    pass

# 用於「更新」排程的模型
class MailScheduleUpdate(BaseModel):
    progcode: Optional[str] = Field(None, max_length=200)
    sender: Optional[str] = Field(None, max_length=200)
    sendername: Optional[str] = Field(None, max_length=200)
    recipients: Optional[str] = None
    cc: Optional[str] = None
    bcc: Optional[str] = None
    replyto: Optional[str] = Field(None, max_length=200)
    subject: Optional[str] = Field(None, max_length=500)
    body: Optional[str] = None
    bodytype: Optional[str] = None
    priority: Optional[str] = None
    encoding: Optional[str] = Field(None, max_length=50)
    attachmentpaths: Optional[str] = None
    smtphost: Optional[str] = Field(None, max_length=200)
    smtpport: Optional[int] = None
    smtpusername: Optional[str] = Field(None, max_length=200)
    smtppassword: Optional[str] = Field(None, max_length=500)
    smtpenablessl: Optional[bool] = None
    smtptimeoutseconds: Optional[int] = None
    isenabled: Optional[bool] = None
    schedulecron: Optional[str] = Field(None, max_length=100)
    modifiedby: Optional[str] = Field(None, max_length=100)
    remark: Optional[str] = None

# 【新增】用於「更新」排程狀態的模型
class MailScheduleStatusUpdate(BaseModel):
    is_enabled: bool = Field(..., description="是否啟用任務")

# 用於「讀取」排程資料並從 API 回應的模型 (包含資料庫產生的欄位)
class MailSchedule(MailScheduleBase):
    id: int
    lastexecutetime: Optional[datetime] = None
    lastsuccesstime: Optional[datetime] = None
    lasterrormessage: Optional[str] = None
    executecount: int
    successcount: int
    failurecount: int
    nextexecutetime: Optional[datetime] = None
    createddate: datetime
    modifieddate: datetime
    executionstatus: str
    currentretrycount: int

    class Config:
        orm_mode = True

