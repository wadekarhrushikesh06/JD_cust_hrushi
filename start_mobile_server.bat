@echo off
title Resume Tailor Mobile Server
cd /d "%~dp0"
echo ========================================================
echo Starting Resume Tailor Mobile Server...
echo ========================================================
"C:\Users\admin\AppData\Local\Programs\Python\Python310\python.exe" scripts\mobile_server.py
pause
