@echo off
cls
choice /t 5 /d y /n >nul
@echo Started: %date% %time%
:start
python fishing.py
@echo Reset: %date% %time%
goto start