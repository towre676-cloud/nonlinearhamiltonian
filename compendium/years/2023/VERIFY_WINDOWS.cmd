@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 verify_all.py
) else (
  python verify_all.py
)
echo.
pause
