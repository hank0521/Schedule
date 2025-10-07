"""
SQLAlchemy Model for the tblschedulemail table.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base # 修正 Base 導入路徑以符合專案結構

class MailSchedule(Base):
    __tablename__ = "tblschedulemail"

    id = Column(Integer, primary_key=True, index=True)
    progcode = Column(String(200), nullable=False, index=True)
    sender = Column(String(200), nullable=False)
    sendername = Column(String(200))
    recipients = Column(Text, nullable=False)
    cc = Column(Text)
    bcc = Column(Text)
    replyto = Column(String(200))
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    bodytype = Column(String(10), default='HTML')
    priority = Column(String(10), default='Normal')
    encoding = Column(String(50), default='UTF-8')
    attachmentpaths = Column(Text)
    smtphost = Column(String(200))
    smtpport = Column(Integer, default=587)
    smtpusername = Column(String(200))
    smtppassword = Column(String(500))
    smtpenablessl = Column(Boolean, default=True)
    smtptimeoutseconds = Column(Integer, default=30)
    lastexecutetime = Column(TIMESTAMP)
    lastsuccesstime = Column(TIMESTAMP)
    lasterrormessage = Column(Text)
    executecount = Column(Integer, default=0)
    successcount = Column(Integer, default=0)
    failurecount = Column(Integer, default=0)
    isenabled = Column(Boolean, default=True, index=True)
    schedulecron = Column(String(100))
    nextexecutetime = Column(TIMESTAMP, index=True)
    createdby = Column(String(100))
    createddate = Column(TIMESTAMP, server_default=func.now(), index=True)
    modifiedby = Column(String(100))
    modifieddate = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    remark = Column(Text)
    executionstatus = Column(String(20), default='Pending', index=True)
    currentretrycount = Column(Integer, default=0)

