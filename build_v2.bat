cd "ColdEmailApp/frontend"

echo Copying embedded python to frontend build context...
if exist python_embedded rmdir /s /q python_embedded
xcopy /E /I /Y "..\python_embedded" "python_embedded"

echo Copying backend to frontend build context...
if exist backend rmdir /s /q backend
xcopy /E /I /Y "..\backend" "backend"

call npm run build
call npx electron-packager . "ColdEmailReach" --platform=win32 --arch=x64 --out=packaged_app --overwrite
cd ../..
python -c "import shutil; shutil.make_archive('app_payload', 'zip', 'c:/Users/Marcio/Desktop/Cold Email App/ColdEmailApp/frontend/packaged_app/ColdEmailReach-win32-x64')"
pyinstaller --noconfirm --onefile --windowed --uac-admin --icon "app_icon.ico" --name "ColdEmailReachSetup" --version-file "version_info.txt" --add-data "app_payload.zip;." --add-data "installer_sidebar_v2.png;." --add-data "app_icon.ico;." installer.py
