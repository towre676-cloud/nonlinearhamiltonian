@echo off
set PYTHONUTF8=1
cd /d "%~dp0"
py -3 --version >nul 2>nul
if errorlevel 1 (
  python verify_all.py
) else (
  py -3 verify_all.py
)
pause
