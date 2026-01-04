
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, delete
from typing import List

from database import init_db, get_db, DATABASE_URL
from models import Lead, Settings
from schemas import LeadResponse, SettingsUpdate
from services.import_service import process_import
import traceback
from services.email_service import EmailService
from services.inbox_service import InboxService
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def read_root():
    print(f"Server Root Check: Running. DB Path: {DATABASE_URL}")
    return {"message": "Hello from Cold Email App Backend!", "status": "running"}

class BatchDeleteRequest(BaseModel):
    lead_ids: List[int] = []
    all: bool = False

@app.post("/leads/delete")
async def delete_leads(request: BatchDeleteRequest, db: AsyncSession = Depends(get_db)):
    if request.all:
        # Delete all leads
        await db.execute(delete(Lead))
        await db.commit()
        return {"message": "All leads deleted", "deleted_count": -1}
    
    if request.lead_ids:
        # Delete specific leads
        stmt = delete(Lead).where(Lead.id.in_(request.lead_ids))
        result = await db.execute(stmt)
        await db.commit()
        return {"message": f"Deleted {result.rowcount} leads", "deleted_count": result.rowcount}
    
    return {"message": "No leads selected", "deleted_count": 0}

@app.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    # Total Leads
    result = await db.execute(select(func.count(Lead.id)))
    total_leads = result.scalar() or 0
    
    # Emails Sent (All time from logs)
    # Correcting model import inside function if needed or rely on top level
    from models import AppLog # ensuring import
    
    sent_res = await db.execute(select(func.count(AppLog.id)).where(AppLog.event_type == 'SENT'))
    emails_sent = sent_res.scalar() or 0
    
    # Replies (Events)
    reply_res = await db.execute(select(func.count(AppLog.id)).where(AppLog.event_type == 'REPLY'))
    replies = reply_res.scalar() or 0
    
    # Rate
    reply_rate = 0.0
    if emails_sent > 0:
        reply_rate = round((replies / emails_sent) * 100, 1)
    
    return {
        "emails_sent": emails_sent, 
        "replies_received": replies,
        "reply_rate": reply_rate,
        "active_leads": total_leads
    }

@app.get("/leads", response_model=List[LeadResponse])
async def get_leads(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    print(f"DEBUG: Fetching leads skip={skip} limit={limit}")
    result = await db.execute(select(Lead).order_by(Lead.id).offset(skip).limit(limit))
    leads = result.scalars().all()
    print(f"DEBUG: Returning {len(leads)} leads")
    return leads

@app.post("/import", status_code=201)
async def import_file(response: Response, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        count = await process_import(text_content, file.filename, db)
        return {"message": f"Successfully imported {count} leads", "imported_count": count}
    except Exception as e:
        print(f"IMPORT ERROR: {e}")
        traceback.print_exc()
        response.status_code = 500
        return {"message": f"Import Failed: {str(e)}", "imported_count": 0}

# --- Settings ---
@app.get("/settings")
async def get_settings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Settings).limit(1))
    settings = result.scalars().first()
    if not settings:
        settings = Settings(daily_limit=50)
        db.add(settings)
        await db.commit()
    return settings

@app.put("/settings")
async def update_settings(update_data: SettingsUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Settings).limit(1))
    settings = result.scalars().first()
    if not settings:
        settings = Settings()
        db.add(settings)
    
    if update_data.smtp_user is not None: settings.smtp_user = update_data.smtp_user
    if update_data.smtp_password is not None: settings.smtp_password = update_data.smtp_password
    if update_data.email_template_body is not None: settings.email_template_body = update_data.email_template_body
    if update_data.daily_limit is not None: settings.daily_limit = update_data.daily_limit
    
    await db.commit()
    return {"status": "updated"}

# --- Actions ---
@app.post("/campaign/start")
async def start_campaign(db: AsyncSession = Depends(get_db)):
    """
    Trigger a batch send (5 emails). 
    Frontend calls this repeatedly or we implement loop later.
    """
    service = EmailService(db)
    count = await service.run_batch(batch_size=5)
    return {"status": "completed", "emails_sent": count}

    service = InboxService(db)
    result = await service.sync_inbox()
    return result


if __name__ == "__main__":
    import uvicorn
    # Use app object directly to avoid import string issues in frozen app
    uvicorn.run(app, host="127.0.0.1", port=8000)
