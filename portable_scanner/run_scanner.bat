@echo off
REM ============================================================
REM Document Scanner - Run Script
REM ============================================================

echo.
echo =============================================
echo Document Scanner
echo =============================================
echo.
echo Usage:
echo   scanner.exe                          (defaults)
echo   scanner.exe -i ./scans -o ./output   (custom folders)
echo   scanner.exe -m 3000 -q 95            (custom size/quality)
echo.
echo Defaults:
echo   Input:  ./scans
echo   Output: ./output
echo   Max Size: 2000px
echo   Quality: 90
echo.
echo =============================================
echo.

REM Create folders if they don't exist
if not exist "scans" mkdir scans
if not exist "output" mkdir output

REM Run with optional arguments
scanner.exe %*
