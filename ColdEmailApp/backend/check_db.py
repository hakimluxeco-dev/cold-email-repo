import asyncio
from database import get_db, init_db
from sqlalchemy.future import select
from models import Lead
from sqlalchemy import func

async def check_leads():
    async for db in get_db():
        result = await db.execute(select(func.count(Lead.id)))
        count = result.scalar()
        print(f"Total Leads in DB: {count}")
        
        if count > 0:
            result = await db.execute(select(Lead).limit(5))
            leads = result.scalars().all()
            print("First 5 leads:")
            for lead in leads:
                print(f"ID: {lead.id}, Name: {lead.name}, Email: {lead.email}, Status: {lead.status}")
        break

if __name__ == "__main__":
    asyncio.run(check_leads())
