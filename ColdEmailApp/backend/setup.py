from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but some modules need help.
build_exe_options = {
    "packages": ["os", "sys", "uvicorn", "fastapi", "pydantic", "starlette", "email", "imap_tools", "sqlalchemy", "aiosqlite"],
    "excludes": ["tkinter", "unittest"],
    "include_files": []
}

setup(
    name="ColdEmailBackend",
    version="1.0",
    description="Backend for Cold Email App",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name="backend_main.exe", base=None)]
)
