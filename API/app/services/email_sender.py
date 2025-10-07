"""
核心郵件發送服務
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Tuple

from app.models import mail as models_mail
from app.core.logger import get_logger
from app.config import settings # 導入設定

logger = get_logger(__name__)

async def send_schedule_mail(schedule: models_mail.MailSchedule) -> Tuple[bool, str]:
    """
    根據排程任務的設定發送郵件。
    如果任務本身沒有 SMTP 設定，則使用 .env 中的預設設定。
    """
    # 決定要使用的 SMTP 設定
    # 優先使用資料庫中的設定，如果為空，則 fallback 到 .env 的預設值
    host = schedule.smtphost or settings.DEFAULT_SMTP_HOST
    port = schedule.smtpport or settings.DEFAULT_SMTP_PORT
    username = schedule.smtpusername or settings.DEFAULT_SMTP_USER
    password = schedule.smtppassword or settings.DEFAULT_SMTP_PASS
    use_ssl = schedule.smtpenablessl if schedule.smtpenablessl is not None else settings.DEFAULT_SMTP_USE_SSL

    # 如果最終沒有任何有效的 SMTP 主機設定，則返回失敗
    if not host:
        return False, "SMTP 主機未設定 (資料庫或 .env 中均未提供)"

    logger.info(f"準備發送郵件任務 ID: {schedule.id}，使用 SMTP 主機: {host}:{port}")

    try:
        # 建立郵件訊息
        msg = MIMEMultipart()
        sender_name = schedule.sendername or schedule.sender
        msg['From'] = f'"{Header(sender_name, "utf-8").encode()}" <{schedule.sender}>'
        msg['To'] = schedule.recipients
        if schedule.cc:
            msg['Cc'] = schedule.cc
        if schedule.bcc:
            msg['Bcc'] = schedule.bcc
        msg['Subject'] = Header(schedule.subject, 'utf-8')

        # 郵件內容
        body_type = 'html' if schedule.bodytype.upper() == 'HTML' else 'plain'
        msg.attach(MIMEText(schedule.body, body_type, schedule.encoding))

        # 組合收件人列表
        all_recipients = schedule.recipients.split(';')
        if schedule.cc:
            all_recipients.extend(schedule.cc.split(';'))
        if schedule.bcc:
            all_recipients.extend(schedule.bcc.split(';'))
        
        # 建立 SMTP 連線並發送
        with smtplib.SMTP(host, port, timeout=schedule.smtptimeoutseconds) as server:
            if use_ssl:
                server.starttls()
            if username and password:
                server.login(username, password)
            
            server.sendmail(schedule.sender, all_recipients, msg.as_string())

        logger.info(f"郵件任務 ID: {schedule.id} 已成功發送。")
        return True, "郵件發送成功"

    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP 認證失敗: {e}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"發送郵件時發生未預期錯誤: {e}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

