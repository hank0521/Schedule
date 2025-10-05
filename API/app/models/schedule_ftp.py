"""FTP 排程任務 Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, BigInteger
from sqlalchemy.sql import func
from app.models.base import Base


class ScheduleFtp(Base):
    """FTP 排程任務資料表"""
    __tablename__ = "tblscheduleftp"

    # 主鍵
    id = Column("Id", Integer, primary_key=True, index=True, autoincrement=True)

    # 基本資訊
    prog_code = Column("ProgCode", String(200), nullable=False, index=True)

    # FTP 連線設定
    ftp_host = Column("FtpHost", String(200), nullable=False)
    ftp_port = Column("FtpPort", Integer, default=21)
    ftp_username = Column("FtpUsername", String(200), nullable=False)
    ftp_password = Column("FtpPassword", String(500), nullable=True)
    ftp_protocol = Column("FtpProtocol", String(10), default="FTP")
    ftp_mode = Column("FtpMode", String(10), default="Passive")
    ftp_encoding = Column("FtpEncoding", String(50), default="UTF-8")
    ftp_timeout_seconds = Column("FtpTimeoutSeconds", Integer, default=30)

    # 傳輸設定
    local_file_path = Column("LocalFilePath", Text, nullable=False)
    remote_file_path = Column("RemoteFilePath", Text, nullable=False)
    transfer_mode = Column("TransferMode", String(10), default="Binary")
    overwrite_existing = Column("OverwriteExisting", Boolean, default=True)
    create_remote_directory = Column("CreateRemoteDirectory", Boolean, default=True)
    delete_local_after_upload = Column("DeleteLocalAfterUpload", Boolean, default=False)

    # 進階設定
    retry_count = Column("RetryCount", Integer, default=0)
    retry_interval_seconds = Column("RetryIntervalSeconds", Integer, default=5)

    # 執行狀態
    execution_status = Column("ExecutionStatus", String(20), default="Pending", index=True)
    current_retry_count = Column("CurrentRetryCount", Integer, default=0)

    # 執行結果
    last_execute_time = Column("LastExecuteTime", TIMESTAMP, nullable=True)
    last_success_time = Column("LastSuccessTime", TIMESTAMP, nullable=True)
    last_transferred_files = Column("LastTransferredFiles", Text, nullable=True)
    last_transferred_bytes = Column("LastTransferredBytes", BigInteger, nullable=True)
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
        return f"<ScheduleFtp(id={self.id}, prog_code={self.prog_code}, ftp_host={self.ftp_host})>"
