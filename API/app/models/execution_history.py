"""執行歷史記錄 Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, BigInteger, JSON
from sqlalchemy.sql import func
from app.models.base import Base


class ScheduleExecutionHistory(Base):
    """執行歷史記錄資料表"""
    __tablename__ = "tblscheduleexecutionhistory"

    # 主鍵
    id = Column("Id", Integer, primary_key=True, index=True, autoincrement=True)

    # 關聯資訊
    service_type = Column("ServiceType", String(20), nullable=False, index=True)
    service_task_id = Column("ServiceTaskId", Integer, nullable=False, index=True)
    prog_code = Column("ProgCode", String(200), nullable=True)

    # 執行資訊
    start_time = Column("StartTime", TIMESTAMP, nullable=False, index=True)
    end_time = Column("EndTime", TIMESTAMP, nullable=True)
    duration_ms = Column("DurationMs", Integer, nullable=True)
    is_success = Column("IsSuccess", Boolean, nullable=False, index=True)
    error_message = Column("ErrorMessage", Text, nullable=True)

    # HTTP 專用欄位
    http_status = Column("HttpStatus", Integer, nullable=True)
    response_size = Column("ResponseSize", Integer, nullable=True)

    # Mail 專用欄位
    emails_sent = Column("EmailsSent", Integer, nullable=True)

    # FTP 專用欄位
    files_transferred = Column("FilesTransferred", Integer, nullable=True)
    bytes_transferred = Column("BytesTransferred", BigInteger, nullable=True)

    # 執行結果詳情
    execution_details = Column("ExecutionDetails", JSON, nullable=True)

    # 系統欄位
    created_date = Column("CreatedDate", TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<ScheduleExecutionHistory(id={self.id}, service_type={self.service_type}, is_success={self.is_success})>"
