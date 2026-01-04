import asyncio
from database import init_db, get_db
from models import Lead
from sqlalchemy import select, delete, func

async def debug_delete():
    print("Initializing DB...")
    await init_db()
    
    # 1. Create a dummy lead
    print("Creating dummy lead...")
    dummy_lead = Lead(name="Delete Me", email="delete@example.com", status="Pending")
    
    async for db in get_db():
        # Check if exists first and clean up
        stmt = delete(Lead).where(Lead.email == "delete@example.com")
        await db.execute(stmt)
        await db.commit()
        
        db.add(dummy_lead)
        await db.commit()
        await db.refresh(dummy_lead)
        lead_id = dummy_lead.id
        print(f"Created lead with ID: {lead_id}")
        
        # 2. Try to delete it using the logic from main.py
        print(f"Attempting to delete lead {lead_id}...")
        
        # main.py logic:
        # stmt = delete(Lead).where(Lead.id.in_(request.lead_ids))
        # lead_ids is a list of ints.
        
        lead_ids = [lead_id]
        stmt = delete(Lead).where(Lead.id.in_(lead_ids))
        result = await db.execute(stmt)
        await db.commit()
        
        print(f"Rows deleted: {result.rowcount}")
        
        # 3. Verify it's gone
        result = await db.execute(select(Lead).where(Lead.id == lead_id))
        check = result.scalars().first()
        
        if check is None:
            print("SUCCESS: Lead verified deleted.")
        else:
            print("FAILURE: Lead still exists!")
            
        break

if __name__ == "__main__":
    asyncio.run(debug_delete())
