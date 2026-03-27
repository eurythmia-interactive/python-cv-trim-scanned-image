@echo off
REM ============================================================
REM Build script for Windows - Run ONCE to create scanner.exe
REM Prerequisites: Python 3.12+ must be installed
REM ============================================================

echo =============================================
echo Document Scanner - Build Script
echo =============================================
echo.

REM Step 1: Check Python installation
echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+ from https://python.org
    pause
    exit /b 1
)
echo.

REM Step 2: Install PyInstaller
echo [2/3] Installing PyInstaller (one-time)...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller. Check internet connection.
    pause
    exit /b 1
)
echo.

REM Step 3: Build the executable
echo [3/3] Building scanner.exe...
cd scanner_src
pyinstaller --onefile --name scanner --console --noconfirm scanner.py
cd ..

echo.
echo =============================================
if exist "scanner_src\dist\scanner.exe" (
    echo BUILD SUCCESSFUL!
    echo.
    echo Your executable is at:
    echo   scanner_src\dist\scanner.exe
    echo.
    echo Next step: Copy scanner.exe to the main folder
    echo and run run_scanner.bat
) else (
    echo BUILD FAILED! Check errors above.
)
echo =============================================
pause
