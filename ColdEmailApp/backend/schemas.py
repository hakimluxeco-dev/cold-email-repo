from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    source: Optional[str] = None
    icebreaker: Optional[str] = None
    status: Optional[str] = "Pending"

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    last_contacted: Optional[datetime]

    class Config:
        orm_mode = True

class SettingsUpdate(BaseModel):
    smtp_user: Optional[str]
    smtp_password: Optional[str]
    email_template_body: Optional[str]
    daily_limit: Optional[int]

    class Config:
        extra = "ignore"
