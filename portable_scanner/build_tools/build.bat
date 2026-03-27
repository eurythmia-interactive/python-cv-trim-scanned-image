@echo off
REM Build script for Windows - Run ONCE to create scanner.exe
REM Requires Python installed on Windows (download from python.org)

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
cd scanner_src
pyinstaller --onefile --name scanner --console --noconfirm scanner.py
cd ..

echo.
echo Build complete! Your executable is at:
echo   scanner_src\dist\scanner.exe
echo.
echo Copy scanner.exe to your target folder and run it.
pause
