@echo off
setlocal

echo ==========================================
echo  Building Virtual Assistant executables
echo ==========================================

REM Ensure we are in project root
cd /d %~dp0

REM Clean previous builds
echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

REM Build Assistant Core
echo.
echo [1/2] Building AssistantCore.exe
pyinstaller ^
  --noconsole ^
  --onefile ^
  main.py ^
  --name AssistantCore

if errorlevel 1 (
  echo.
  echo ERROR: Failed to build AssistantCore.exe
  pause
  exit /b 1
)

REM Build GUI
echo.
echo [2/2] Building VirtualAssistantGUI.exe
pyinstaller ^
  --noconsole ^
  --onefile ^
  --collect-all assistant ^
  --paths . ^
  assistant/gui/configurator.py ^
  --name VirtualAssistantGUI

if errorlevel 1 (
  echo.
  echo ERROR: Failed to build VirtualAssistantGUI.exe
  pause
  exit /b 1
)

echo.
echo ==========================================
echo  Build completed successfully
echo ==========================================
echo.

echo Output files:
echo   dist\AssistantCore.exe
echo   dist\VirtualAssistantGUI.exe
echo.

pause
endlocal
