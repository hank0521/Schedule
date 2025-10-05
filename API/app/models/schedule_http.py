"""HTTP 排程任務 Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, JSON
from sqlalchemy.sql import func
from app.models.base import Base


class ScheduleHttp(Base):
    """HTTP 排程任務資料表"""
    __tablename__ = "tblschedulehttp"

    # 主鍵
    id = Column("Id", Integer, primary_key=True, index=True, autoincrement=True)

    # 基本資訊
    prog_code = Column("ProgCode", String(200), nullable=False, index=True)
    url = Column("Url", Text, nullable=False)
    http_method = Column("HttpMethod", String(10), nullable=False, default="GET")

    # 請求設定
    headers = Column("Headers", JSON, nullable=True)
    request_body = Column("RequestBody", Text, nullable=True)
    content_type = Column("ContentType", String(100), default="application/json")
    encoding = Column("Encoding", String(50), default="UTF-8")
    timeout_seconds = Column("TimeoutSeconds", Integer, default=30)

    # 重試設定
    retry_count = Column("RetryCount", Integer, default=0)
    retry_interval_seconds = Column("RetryIntervalSeconds", Integer, default=5)
    expected_http_status = Column("ExpectedHttpStatus", Integer, default=200)

    # 執行狀態
    execution_status = Column("ExecutionStatus", String(20), default="Pending", index=True)
    current_retry_count = Column("CurrentRetryCount", Integer, default=0)

    # 執行結果
    last_execute_time = Column("LastExecuteTime", TIMESTAMP, nullable=True)
    last_http_status = Column("LastHttpStatus", Integer, nullable=True)
    last_response_body = Column("LastResponseBody", Text, nullable=True)
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
        return f"<ScheduleHttp(id={self.id}, prog_code={self.prog_code}, url={self.url})>"
