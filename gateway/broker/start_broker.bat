@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "MOSQ=mosquitto"
if exist "C:\Program Files\mosquitto\mosquitto.exe" set "MOSQ=C:\Program Files\mosquitto\mosquitto.exe"
if exist "C:\Program Files (x86)\mosquitto\mosquitto.exe" set "MOSQ=C:\Program Files (x86)\mosquitto\mosquitto.exe"
"%MOSQ%" -c mosquitto.conf -v
echo.
echo [ERROR] Mosquitto exited. Install it or check the message above.
pause
