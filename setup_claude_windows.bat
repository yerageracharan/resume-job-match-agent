@echo off
setlocal
cd /d "%~dp0"
echo ===============================================
echo Resume Job Match Agent - Claude Desktop setup
echo ===============================================
echo.
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher not found. Install Python 3.11+ and enable PATH.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 (
    echo Could not create the environment. Confirm Python 3.11+ is installed.
    pause
    exit /b 1
  )
)
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
call ".venv\Scripts\python.exe" -m pip install -r requirements-claude.txt
if errorlevel 1 (
  echo Dependency installation failed.
  pause
  exit /b 1
)
call ".venv\Scripts\python.exe" configure_claude.py
if errorlevel 1 (
  echo Claude configuration failed.
  pause
  exit /b 1
)
echo.
echo Setup complete. Fully quit and restart Claude Desktop.
pause
