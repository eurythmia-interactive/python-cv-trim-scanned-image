# Portable Document Scanner

## Quick Start

### Step 1: Build the executable (ONCE on Windows)
1. Make sure Python is installed on your Windows PC (download from python.org)
2. Copy this entire folder to your Windows PC
3. Run `build_tools\build.bat`
4. Wait for "Build complete!" message

### Step 2: Run the scanner
1. Copy `scanner_src\dist\scanner.exe` to this folder
2. Create a `scans` folder and put your scanned images there
3. Create an `output` folder (or it will be created automatically)
4. Run `run_scanner.bat`

## Folder Structure
```
portable_scanner/
├── scanner.exe        <-- The executable (after building)
├── scans/              <-- Put scanned images here
├── output/             <-- Processed images appear here
├── scanner.log         <-- Log file
└── run_scanner.bat     <-- Run this
```

## Requirements
- Windows PC with Python 3.12+ installed (only needed for building)
- No internet required after initial Python installation
