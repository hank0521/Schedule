"""Email 發送客戶端模組"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional
from app.core.logger import get_logger

logger = get_logger(__name__)


class MailClient:
    """Email 發送客戶端類別"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None,
        use_ssl: bool = True,
        timeout: int = 30
    ):
        """
        初始化 Email 客戶端

        Args:
            smtp_host: SMTP 伺服器位址
            smtp_port: SMTP 埠號 (587: TLS, 465: SSL, 25: 無加密)
            smtp_username: SMTP 使用者名稱
            smtp_password: SMTP 密碼
            use_ssl: 是否使用 SSL/TLS
            timeout: 連線超時時間(秒)
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.use_ssl = use_ssl
        self.timeout = timeout

    def _parse_recipients(self, recipients: str) -> List[str]:
        """
        解析收件者字串 (支援分號分隔)

        Args:
            recipients: 收件者字串,多個以分號分隔

        Returns:
            List[str]: 收件者 Email 列表
        """
        return [email.strip() for email in recipients.split(";") if email.strip()]

    def _create_message(
        self,
        sender: str,
        recipients: List[str],
        subject: str,
        body: str,
        body_type: str = "HTML",
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> MIMEMultipart:
        """
        建立郵件訊息物件

        Args:
            sender: 寄件者
            recipients: 收件者列表
            subject: 主旨
            body: 郵件內容
            body_type: 郵件格式 (HTML/TEXT)
            cc: 副本收件者列表
            bcc: 密件副本收件者列表

        Returns:
            MIMEMultipart: 郵件訊息物件
        """
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject

        if cc:
            message["Cc"] = ", ".join(cc)
        if bcc:
            message["Bcc"] = ", ".join(bcc)

        # 設定郵件內容
        mime_type = "html" if body_type.upper() == "HTML" else "plain"
        message.attach(MIMEText(body, mime_type, "utf-8"))

        return message

    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """
        附加檔案到郵件

        Args:
            message: 郵件訊息物件
            file_path: 檔案路徑
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"Attachment file not found: {file_path}")
                return

            with open(path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {path.name}"
            )
            message.attach(part)
            logger.info(f"Attached file: {path.name}")

        except Exception as e:
            logger.error(f"Failed to attach file {file_path}: {e}")
            raise

    async def send_mail(
        self,
        sender: str,
        recipients: str,
        subject: str,
        body: str,
        body_type: str = "HTML",
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        sender_name: Optional[str] = None
    ) -> bool:
        """
        發送郵件

        Args:
            sender: 寄件者 Email
            recipients: 收件者 (多個以分號分隔)
            subject: 主旨
            body: 郵件內容
            body_type: 郵件格式 (HTML/TEXT)
            cc: 副本收件者 (多個以分號分隔)
            bcc: 密件副本收件者 (多個以分號分隔)
            sender_name: 寄件者顯示名稱

        Returns:
            bool: True 表示發送成功, False 表示失敗
        """
        try:
            recipients_list = self._parse_recipients(recipients)
            cc_list = self._parse_recipients(cc) if cc else None
            bcc_list = self._parse_recipients(bcc) if bcc else None

            # 建立郵件
            sender_address = f"{sender_name} <{sender}>" if sender_name else sender
            message = self._create_message(
                sender=sender_address,
                recipients=recipients_list,
                subject=subject,
                body=body,
                body_type=body_type,
                cc=cc_list,
                bcc=bcc_list
            )

            # 所有收件者 (包含 CC 和 BCC)
            all_recipients = recipients_list.copy()
            if cc_list:
                all_recipients.extend(cc_list)
            if bcc_list:
                all_recipients.extend(bcc_list)

            # 發送郵件
            logger.info(f"Sending email to {len(all_recipients)} recipients")

            if self.use_ssl and self.smtp_port == 465:
                # SSL 連線
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.smtp_username,
                    password=self.smtp_password,
                    use_tls=True,
                    timeout=self.timeout
                )
            else:
                # STARTTLS 連線
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.smtp_username,
                    password=self.smtp_password,
                    start_tls=True,
                    timeout=self.timeout
                )

            logger.info("Email sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    async def send_mail_with_attachments(
        self,
        sender: str,
        recipients: str,
        subject: str,
        body: str,
        attachment_paths: str,
        body_type: str = "HTML",
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        sender_name: Optional[str] = None
    ) -> bool:
        """
        發送帶附件的郵件

        Args:
            sender: 寄件者 Email
            recipients: 收件者 (多個以分號分隔)
            subject: 主旨
            body: 郵件內容
            attachment_paths: 附件路徑 (多個以分號分隔)
            body_type: 郵件格式 (HTML/TEXT)
            cc: 副本收件者
            bcc: 密件副本收件者
            sender_name: 寄件者顯示名稱

        Returns:
            bool: True 表示發送成功, False 表示失敗
        """
        try:
            recipients_list = self._parse_recipients(recipients)
            cc_list = self._parse_recipients(cc) if cc else None
            bcc_list = self._parse_recipients(bcc) if bcc else None

            # 建立郵件
            sender_address = f"{sender_name} <{sender}>" if sender_name else sender
            message = self._create_message(
                sender=sender_address,
                recipients=recipients_list,
                subject=subject,
                body=body,
                body_type=body_type,
                cc=cc_list,
                bcc=bcc_list
            )

            # 附加檔案
            attachment_list = [path.strip() for path in attachment_paths.split(";") if path.strip()]
            for file_path in attachment_list:
                self._attach_file(message, file_path)

            # 所有收件者
            all_recipients = recipients_list.copy()
            if cc_list:
                all_recipients.extend(cc_list)
            if bcc_list:
                all_recipients.extend(bcc_list)

            # 發送郵件
            logger.info(f"Sending email with {len(attachment_list)} attachments to {len(all_recipients)} recipients")

            if self.use_ssl and self.smtp_port == 465:
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.smtp_username,
                    password=self.smtp_password,
                    use_tls=True,
                    timeout=self.timeout
                )
            else:
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.smtp_username,
                    password=self.smtp_password,
                    start_tls=True,
                    timeout=self.timeout
                )

            logger.info("Email with attachments sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send email with attachments: {e}")
            return False
