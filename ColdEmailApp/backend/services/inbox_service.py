import imaplib
import email
from email.header import decode_header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Lead, Settings, AppLog
import asyncio
import re

class InboxService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_inbox(self):
        # 1. Get Settings
        result = await self.db.execute(select(Settings).limit(1))
        settings = result.scalars().first()
        
        if not settings or not settings.smtp_user or not settings.smtp_password:
             return {"status": "error", "message": "Credentials missing"}

        # 2. Get all tracked emails efficiently
        leads_result = await self.db.execute(select(Lead.email).where(Lead.status != "Inactive"))
        tracked_emails = set([e.lower() for e in leads_result.scalars().all()])
        
        if not tracked_emails:
            return {"status": "ok", "updates": 0}

        # 3. Fetch Updates (Run blocking IMAP in thread)
        try:
            updates = await asyncio.to_thread(
                self._scan_imap, 
                settings.imap_server, 
                settings.smtp_user, 
                settings.smtp_password,
                tracked_emails
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        # 4. Apply Updates to DB
        count = 0
        for email_addr, new_status in updates.items():
            # Find lead
            lead_res = await self.db.execute(select(Lead).where(Lead.email == email_addr))
            lead = lead_res.scalars().first()
            if lead and lead.status != new_status:
                lead.status = new_status
                count += 1
                # Log it
                self.db.add(AppLog(event_type="REPLY", details=f"Lead {lead.name} status -> {new_status}"))
        
        await self.db.commit()
        return {"status": "ok", "updates": count}

    def _scan_imap(self, server, user, password, tracked_emails):
        updates = {}
        
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        mail.select("inbox")
        
        # Check Replies (Scanning last 50 like original)
        status, messages = mail.search(None, 'ALL')
        if status == "OK":
            email_ids = messages[0].split()
            # Look at last 50
            for num in email_ids[-50:]:
                try:
                    res, msg_data = mail.fetch(num, "(RFC822)")
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    from_header = msg.get("From")
                    sender = self._extract_email(from_header)
                    
                    if sender and sender in tracked_emails:
                        subject = msg.get("Subject", "").lower()
                        body = self._get_body(msg).lower()
                        full_text = subject + " " + body
                        
                        # Keyword Logic
                        if any(x in full_text for x in ["stop", "unsubscribe", "remove"]):
                            updates[sender] = "Not Interested"
                        elif any(x in full_text for x in ["interested", "price", "call", "meet"]):
                            updates[sender] = "Interested"
                        else:
                            # Default if they reply at all
                            updates[sender] = "Interested"
                except:
                    continue
                    
        mail.close()
        mail.logout()
        return updates

    def _extract_email(self, header):
        match = re.search(r'<(.+?)>', header)
        if match:
            return match.group(1).lower().strip()
        if "@" in header:
            return header.lower().strip()
        return None

    def _get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(errors='ignore')
        else:
            return msg.get_payload(decode=True).decode(errors='ignore')
        return ""
