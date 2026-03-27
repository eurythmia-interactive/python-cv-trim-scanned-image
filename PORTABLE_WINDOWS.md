# Portable Windows Deployment Guide

## Overview

This document explains how to run the document scanner on a **Windows machine with no Python installed and no internet connection**.

The solution uses **PyInstaller** to create a standalone `.exe` that bundles Python + all libraries into a single executable file.

---

## Method: Build Once, Run Everywhere

### Step 1: One-Time Python Installation (on any Windows PC with internet)

1. Download Python 3.12+ from https://www.python.org/downloads/
2. Install it on your Windows PC
3. Make sure to check "Add Python to PATH" during installation

### Step 2: Copy Project to Windows PC

Copy the entire `portable_scanner/` folder to your target Windows machine.

```
portable_scanner/
├── scanner_src/       # Python source files
│   ├── scanner.py
│   ├── detector.py
│   ├── warp.py
│   ├── saver.py
│   └── watcher.py
├── build_tools/
│   └── build.bat      # Build script (RUN ONCE)
├── scans/             # Place scanned images here
├── output/            # Processed images appear here
├── run_scanner.bat    # Run this to start scanner
└── README.txt
```

### Step 3: Build the Executable (RUN ONCE)

1. Open Command Prompt (cmd.exe)
2. Navigate to the `portable_scanner` folder
3. Run the build script:

```
cd portable_scanner
build_tools\build.bat
```

4. Wait for "Build complete!" message (takes 2-5 minutes)

The executable will be created at:
```
scanner_src\dist\scanner.exe
```

### Step 4: Run the Scanner (Forever, no Python needed)

1. Copy `scanner_src\dist\scanner.exe` to the `portable_scanner` folder
2. Double-click `run_scanner.bat`

Or from command prompt:
```
scanner.exe
```

---

## Usage

### Folder Structure When Running

```
portable_scanner/
├── scanner.exe        # The standalone executable
├── scans/             # Put scanned images (.jpg, .png, .tiff) here
├── output/            # Processed images appear here
└── scanner.log        # Log file with processing results
```

### How It Works

1. Place scanned images in the `scans/` folder
2. The scanner automatically detects new files
3. Documents are cropped, perspective-corrected, and saved to `output/`
4. Check `scanner.log` for processing status

### Processing Log

The `scanner.log` file shows:
- `SUCCESS: input.jpg -> output.jpg` when processed
- `SKIPPED: image.jpg - Reason` when image is rejected
- `FAILURE: image.jpg - Reason` on errors

### Supported Image Formats

- `.jpg` / `.jpeg`
- `.png`
- `.tiff` / `.tif`

### What Gets Rejected

- Images with no document detected (all black, no white paper)
- Images where the document is upside-down
- Files that are still being written (scanner file-in-use)

---

## Troubleshooting

### "DLL not found" or "Import error" on Windows

Make sure you copied the entire `dist/` folder contents, not just the `.exe`. Some DLLs may be alongside the executable.

### No images processed

1. Check `scanner.log` for error messages
2. Make sure images are in the `scans/` folder
3. Verify images are `.jpg`, `.png`, or `.tiff`

### Scanner runs but closes immediately

Run from command prompt to see error messages:
```
scanner.exe
```

### Images upside-down are rejected

The scanner does not support upside-down documents. Place documents in the correct orientation before scanning.

---

## System Requirements

### For Building (one-time only)
- Windows 10/11
- Python 3.12+ installed
- Internet connection (to install PyInstaller and dependencies)

### For Running (no installation needed)
- Windows 10/11
- No Python required
- No internet required
- ~500MB disk space for the bundled executable
