"""Mail 排程任務 Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base


class ScheduleMail(Base):
    """Mail 排程任務資料表"""
    __tablename__ = "tblschedulemail"

    # 主鍵
    id = Column("Id", Integer, primary_key=True, index=True, autoincrement=True)

    # 基本資訊
    prog_code = Column("ProgCode", String(200), nullable=False, index=True)

    # 郵件設定
    sender = Column("Sender", String(200), nullable=False)
    sender_name = Column("SenderName", String(200), nullable=True)
    recipients = Column("Recipients", Text, nullable=False)
    cc = Column("CC", Text, nullable=True)
    bcc = Column("BCC", Text, nullable=True)
    reply_to = Column("ReplyTo", String(200), nullable=True)

    # 郵件內容
    subject = Column("Subject", String(500), nullable=False)
    body = Column("Body", Text, nullable=False)
    body_type = Column("BodyType", String(10), default="HTML")
    priority = Column("Priority", String(10), default="Normal")
    encoding = Column("Encoding", String(50), default="UTF-8")

    # 附件設定
    attachment_paths = Column("AttachmentPaths", Text, nullable=True)

    # SMTP 設定
    smtp_host = Column("SmtpHost", String(200), nullable=True)
    smtp_port = Column("SmtpPort", Integer, default=587)
    smtp_username = Column("SmtpUsername", String(200), nullable=True)
    smtp_password = Column("SmtpPassword", String(500), nullable=True)
    smtp_enable_ssl = Column("SmtpEnableSsl", Boolean, default=True)
    smtp_timeout_seconds = Column("SmtpTimeoutSeconds", Integer, default=30)

    # 執行狀態
    execution_status = Column("ExecutionStatus", String(20), default="Pending", index=True)
    current_retry_count = Column("CurrentRetryCount", Integer, default=0)

    # 執行結果
    last_execute_time = Column("LastExecuteTime", TIMESTAMP, nullable=True)
    last_success_time = Column("LastSuccessTime", TIMESTAMP, nullable=True)
    last_error_message = Column("LastErrorMessage", Text, nullable=True)
    execute_count = Column("ExecuteCount", Integer, default=0)
    success_count = Column("SuccessCount", Integer, default=0)
    failure_count = Column("FailureCount", Integer, default=0)

    # 排程設定
    is_enabled = Column("IsEnabled", Boolean, default=True, index=True)
    schedule_cron = Column("ScheduleCron", String(100), nullable=True)
    next_execute_time = Column("NextExecuteTime", TIMESTAMP, nullable=True, index=True)

    # 系統欄位
    created_by = Column("CreatedBy", String(100), nullable=True)
    created_date = Column("CreatedDate", TIMESTAMP, server_default=func.now(), index=True)
    modified_by = Column("ModifiedBy", String(100), nullable=True)
    modified_date = Column("ModifiedDate", TIMESTAMP, onupdate=func.now())
    remark = Column("Remark", Text, nullable=True)

    def __repr__(self):
        return f"<ScheduleMail(id={self.id}, prog_code={self.prog_code}, recipients={self.recipients})>"
