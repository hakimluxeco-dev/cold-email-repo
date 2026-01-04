
cd "ColdEmailApp/frontend"
call npm run build
call npx electron-packager . "ColdEmailReach" --platform=win32 --arch=x64 --out=packaged_app --overwrite
cd ../..
python -c "import shutil; shutil.make_archive('app_payload', 'zip', 'c:/Users/Marcio/Desktop/Cold Email App/ColdEmailApp/frontend/packaged_app/ColdEmailReach-win32-x64')"
pyinstaller --noconfirm --onefile --windowed --uac-admin --icon "app_icon.ico" --name "ColdEmailReachSetup" --version-file "version_info.txt" --add-data "app_payload.zip;." --add-data "installer_sidebar_v2.png;." --add-data "app_icon.ico;." installer.py
