import asyncio
from services.import_service import _parse_markdown
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import MagicMock

# Validation Test
content = """
| Email Address | Business Name |
|---|---|
| test@example.com | Test Corp |
"""

async def run_test():
    # Mock DB
    db = MagicMock(spec=AsyncSession)
    # Mock execution result to always return None (no existing lead)
    # This involves complex async mocking, but for parsing testing 
    # we mainly want to see if it even TRIES to add.
    
    # Actually, simpler to just run the parser logic in isolation or modify import_service temporarily?
    # No, let's just create a quick direct test of the logic by copying the function here 
    # or importing it if we can run this script in context.
    
    # We can use the actual service if we mock the DB correctly.
    db.execute = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    
    # We need to mock the async execute return
    async def async_execute(*args, **kwargs):
        m = MagicMock()
        m.scalars.return_value.first.return_value = None
        return m
    
    db.execute.side_effect = async_execute
    
    print("Testing Markdown Parse with Email at Index 0...")
    count = await _parse_markdown(content, db)
    print(f"Imported Count: {count}")
    
    if count == 0:
        print("FAILED: Did not import row.")
    else:
        print("SUCCESS: Imported row.")

if __name__ == "__main__":
    asyncio.run(run_test())
