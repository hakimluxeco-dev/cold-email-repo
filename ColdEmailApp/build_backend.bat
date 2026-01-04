@echo off
echo Building Backend...
cd backend
pip install pyinstaller
pyinstaller --noconfirm --onefile --clean ^
    --name backend_main ^
    --distpath ./dist ^
    --workpath ./build ^
    --hidden-import=uvicorn.logging ^
    --hidden-import=uvicorn.loops ^
    --hidden-import=uvicorn.loops.auto ^
    --hidden-import=uvicorn.protocols ^
    --hidden-import=uvicorn.protocols.http ^
    --hidden-import=uvicorn.protocols.http.auto ^
    --hidden-import=uvicorn.lifespan ^
    --hidden-import=uvicorn.lifespan.on ^
    --hidden-import=sqlalchemy.sql.default_comparator ^
    --hidden-import=aiosqlite ^
    main.py

echo Backend Build Complete.
pause
