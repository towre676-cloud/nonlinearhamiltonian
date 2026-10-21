@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
py -3 -X utf8 -S verify_all.py
set VERIFY_EXIT=%ERRORLEVEL%
pause
exit /b %VERIFY_EXIT%
