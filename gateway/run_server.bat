@echo off
chcp 65001 >nul
set "PYTHON=D:\CodeTools\conda_envs\freshchain\python.exe"
if not exist "%PYTHON%" (
    echo [ERROR] Python not found: %PYTHON%
    echo Please run: conda activate D:\CodeTools\conda_envs\freshchain
    pause
    exit /b 1
)
cd /d "%~dp0"
echo ============================================
echo FreshChain Gateway
echo URL: http://127.0.0.1:8080
echo Press Ctrl+C to stop this window.
echo ============================================
"%PYTHON%" server.py --demo --host 127.0.0.1 --port 8080
echo.
echo [ERROR] Server exited. See the message above.
pause
