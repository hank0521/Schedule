"""Pydantic 資料驗證模型 (Schemas) for Mail Schedule"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# 用於更新啟用/停用狀態的 Pydantic 模型
class MailScheduleStatusUpdate(BaseModel):
    is_enabled: bool

# 基礎模型，定義所有 Mail 排程共用的欄位
class MailScheduleBase(BaseModel):
    progcode: str = Field(..., max_length=200)
    sender: EmailStr = Field(..., max_length=200)
    sendername: Optional[str] = Field(None, max_length=200)
    recipients: str
    cc: Optional[str] = None
    bcc: Optional[str] = None
    replyto: Optional[EmailStr] = Field(None, max_length=200)
    subject: str = Field(..., max_length=500)
    body: str
    bodytype: str = Field("HTML", max_length=10)
    priority: str = Field("Normal", max_length=10)
    encoding: str = Field("UTF-8", max_length=50)
    attachmentpaths: Optional[str] = None
    smtphost: Optional[str] = Field(None, max_length=200)
    smtpport: Optional[int] = 587
    smtpusername: Optional[str] = Field(None, max_length=200)
    smtppassword: Optional[str] = Field(None, max_length=500)
    smtpenablessl: Optional[bool] = True
    smtptimeoutseconds: Optional[int] = 30
    schedulecron: Optional[str] = Field(None, max_length=100)
    remark: Optional[str] = None
    createdby: Optional[str] = Field(None, max_length=100)
    modifiedby: Optional[str] = Field(None, max_length=100)

# 用於建立新 Mail 排程的 Pydantic 模型
class MailScheduleCreate(MailScheduleBase):
    pass

# 用於更新 Mail 排程的 Pydantic 模型
class MailScheduleUpdate(MailScheduleBase):
    pass

# 用於從資料庫讀取並回傳給 API 客戶端的 Pydantic 模型
class MailSchedule(MailScheduleBase):
    id: int
    lastexecutetime: Optional[datetime] = None
    lastsuccesstime: Optional[datetime] = None
    lasterrormessage: Optional[str] = None
    executecount: int = 0
    successcount: int = 0
    failurecount: int = 0
    isenabled: bool = True
    nextexecutetime: Optional[datetime] = None
    createddate: datetime
    modifieddate: datetime
    executionstatus: str = "Pending"
    currentretrycount: int = 0

    class Config:
        # 修正：將 orm_mode 改為 from_attributes 以符合 Pydantic V2 標準
        from_attributes = True

