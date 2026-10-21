@echo off
cd /d "%~dp0"
py -3 -B -X utf8 -S verification\verify_publication.py %*
exit /b %errorlevel%
