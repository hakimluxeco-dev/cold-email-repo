import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import random
import logging

from models import Lead, Settings, AppLog

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = None

    async def get_settings(self):
        result = await self.db.execute(select(Settings).limit(1))
        self.settings = result.scalars().first()
        if not self.settings:
            # Create default settings if missing
            self.settings = Settings(
                 smtp_user="",
                 smtp_password="",
                 daily_limit=50
            )
            self.db.add(self.settings)
            await self.db.commit()
        return self.settings

    async def log_event(self, event_type: str, details: str):
        log = AppLog(event_type=event_type, details=details)
        self.db.add(log)
        await self.db.commit()

    async def send_single_email(self, lead: Lead, subject_template: str, body_template: str):
        settings = await self.get_settings()
        
        if not settings.smtp_user or not settings.smtp_password:
            raise ValueError("SMTP Credentials not configured")

        # Personalize
        subject = subject_template.replace("[Business Name]", lead.name)
        body = body_template.replace("[Business Name]", lead.name)\
                            .replace("[Name]", lead.name)\
                            .replace("[Icebreaker]", lead.icebreaker or "")

        msg = MIMEMultipart()
        msg['From'] = settings.smtp_user
        msg['To'] = lead.email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Sending logic (Sync wrapper for smtplib)
        try:
            # Note: storing smtp connection for reuse would be better, but simpler to connect per batch
            # For strict async, we should use aiosmtplib, but standard smtplib is okay for low volume background tasks if run in executor
            
            # Using asyncio.to_thread for blocking SMTP calls
            await asyncio.to_thread(self._send_sync, settings, msg, lead.email)
            
            # Update Lead
            lead.status = "Contacted"
            lead.last_contacted = datetime.now()
            await self.db.commit()
            
            await self.log_event("SENT", f"Email sent to {lead.email}")
            return True

        except Exception as e:
            await self.log_event("ERROR", f"Failed to send to {lead.email}: {str(e)}")
            return False

    def _send_sync(self, settings, msg, to_email):
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)

    async def run_batch(self, batch_size=5):
        """
        Sends to the next N pending leads. 
        """
        # Get pending leads
        result = await self.db.execute(
            select(Lead).where(Lead.status == "Pending").limit(batch_size)
        )
        leads = result.scalars().all()
        
        if not leads:
            return 0
            
        settings = await self.get_settings()
        count = 0
        
        for lead in leads:
            success = await self.send_single_email(
                lead, 
                settings.email_template_subject, 
                settings.email_template_body
            )
            if success:
                count += 1
                # Add delay if processing multiple (simulate human behavior)
                if count < len(leads):
                     delay = random.randint(10, 30) # Short delay for batch
                     await asyncio.sleep(delay)
        
        return count
