from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    status = Column(String, default="Pending") # Pending, Contacted, Interested, Not Interested, Inactive
    icebreaker = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    meta_data = Column(JSON, nullable=True) # Extras like Phone, Area
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_contacted = Column(DateTime(timezone=True), nullable=True)

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    smtp_user = Column(String, nullable=True)
    smtp_password = Column(String, nullable=True) # Encrypted ideally, plain for now locally
    smtp_server = Column(String, default="smtp.gmail.com")
    smtp_port = Column(Integer, default=587)
    
    imap_server = Column(String, default="imap.gmail.com")
    email_template_subject = Column(String, default="Quick question for [Business Name]")
    email_template_body = Column(Text, default="Hi [Name], ...")
    
    daily_limit = Column(Integer, default=50)
    delay_min = Column(Integer, default=600)
    delay_max = Column(Integer, default=1200)

class AppLog(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    event_type = Column(String) # SENT, ERROR, REPLY, INFO
    details = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
