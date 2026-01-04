@echo off
echo Setting up Python Embeddable Package...
cd ColdEmailApp

REM Create python_embedded folder if it doesn't exist
if not exist python_embedded mkdir python_embedded
cd python_embedded

REM Download Python 3.10 embeddable if not exists
if not exist python.exe (
    echo Downloading Python 3.10 embeddable zip...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10. 11-embed-amd64.zip' -OutFile 'python-embed.zip'"
    echo Extracting Python...
    powershell -Command "Expand-Archive -Path 'python-embed.zip' -DestinationPath '.' -Force"
    del python-embed.zip
)

REM Fix python310._pth to enable site-packages
echo Configuring Python import paths...
(
echo python310.zip
echo .
echo ..
echo 
echo # Uncomment to enable site-packages:
echo import site
) > python310._pth

REM Install pip
if not exist get-pip.py (
    echo Downloading get-pip.py...
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"
)

echo Installing pip...
python.exe get-pip.py --no-warn-script-location

echo Installing backend dependencies...
python.exe -m pip install --no-warn-script-location fastapi==0.115.0 uvicorn==0.31.0 sqlalchemy==2.0.23 aiosqlite==0.19.0 pydantic==2.5.2 python-multipart==0.0.6 email-validator

echo Python embedded setup complete!
cd ..\..
