@echo off
cd /d "%~dp0"
py -3 server.py
if errorlevel 1 (
  echo.
  echo Python could not be started. Install Python 3 from https://www.python.org/downloads/
  pause
)
