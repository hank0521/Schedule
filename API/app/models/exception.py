"""例外記錄 Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base


class ScheduleException(Base):
    """例外記錄資料表"""
    __tablename__ = "tblscheduleexception"

    # 主鍵
    id = Column("Id", Integer, primary_key=True, index=True, autoincrement=True)

    # 關聯資訊
    service_type = Column("ServiceType", String(20), nullable=False, index=True)
    service_task_id = Column("ServiceTaskId", Integer, nullable=False, index=True)
    prog_code = Column("ProgCode", String(200), nullable=True)

    # 例外資訊
    exception_type = Column("ExceptionType", String(100), nullable=True)
    exception_message = Column("ExceptionMessage", Text, nullable=False)
    stack_trace = Column("StackTrace", Text, nullable=True)
    inner_exception = Column("InnerException", Text, nullable=True)

    # HTTP 專用欄位
    http_url = Column("HttpUrl", Text, nullable=True)
    http_method = Column("HttpMethod", String(10), nullable=True)
    http_status = Column("HttpStatus", Integer, nullable=True)

    # Mail 專用欄位
    mail_recipients = Column("MailRecipients", Text, nullable=True)
    mail_subject = Column("MailSubject", String(500), nullable=True)

    # FTP 專用欄位
    ftp_host = Column("FtpHost", String(200), nullable=True)
    ftp_local_path = Column("FtpLocalPath", Text, nullable=True)
    ftp_remote_path = Column("FtpRemotePath", Text, nullable=True)

    # 系統欄位
    occurred_date = Column("OccurredDate", TIMESTAMP, server_default=func.now(), index=True)
    is_resolved = Column("IsResolved", Boolean, default=False, index=True)
    resolved_by = Column("ResolvedBy", String(100), nullable=True)
    resolved_date = Column("ResolvedDate", TIMESTAMP, nullable=True)
    resolve_note = Column("ResolveNote", Text, nullable=True)

    def __repr__(self):
        return f"<ScheduleException(id={self.id}, service_type={self.service_type}, task_id={self.service_task_id})>"
