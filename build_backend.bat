@echo off
echo Building Backend Executable...
cd ColdEmailApp\backend
pyinstaller --onefile --name backend_main --hidden-import=sqlalchemy.ext.asyncio --hidden-import=aiosqlite main.py
echo Backend build complete!
cd ..\..
