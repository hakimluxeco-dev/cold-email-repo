from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

import os
import sys

# Store DB in the application directory (or subdirectory)
# In embedded python, sys.executable is inside python_embedded folder
# We want to go up one level to the root of the app
if getattr(sys, 'frozen', False):
    # PyInstaller
    base_dir = os.path.dirname(sys.executable)
else:
    # Embedded Python or Source
    # sys.executable is .../python_embedded/python.exe
    # We want .../
    # If running from source (dev), main.py location
    if 'python' in os.path.basename(sys.executable).lower():
         # Check if likely embedded
         if 'python_embedded' in sys.executable:
             base_dir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), ".."))
         else:
             # Standard dev
             base_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        # Fallback
        base_dir = os.path.dirname(os.path.abspath(__file__))

db_folder = os.path.join(base_dir, "data")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "app.db")

print(f"DATABASE PATH: {db_path}") # Debug print

DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
