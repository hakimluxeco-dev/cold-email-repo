@echo off
title Johannesburg Outreach Launcher

echo ===================================================
echo   Johannesburg Cold Outreach System - LAUNCHER
echo ===================================================
echo.
echo This script will start two separate agents:
echo 1. The Outreach Agent (Sends emails)
echo 2. The Inbox Manager (Checks for replies)
echo.
echo PRE-FLIGHT CHECK:
echo Ensure you have your 'App Password' ready.
echo.
pause

:: Launch Inbox Manager in a new window
echo Starting Inbox Manager...
start "Inbox Manager (Monitoring...)" cmd /k "color 0B && python process_inbox.py"

:: Launch Email Sender in a new window
echo Starting Outreach Agent...
start "Outreach Agent (Sending...)" cmd /k "color 0A && python send_emails.py"

echo.
echo ===================================================
echo   AGENTS LAUNCHED!
echo ===================================================
echo.
echo Please check the two new windows that opened.
echo You will need to enter your Email and App Password in BOTH windows.
echo.
echo You can close this launcher window now.
pause
