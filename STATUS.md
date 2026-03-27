# Project Status

## Overview

Document scanner pipeline using OpenCV for computer vision. Monitors a folder for scanned images, detects document boundaries, corrects perspective, and outputs cropped images ready for projection.

**Repository:** https://github.com/eurythmia-interactive/python-cv-trim-scanned-image

---

## Development Log

### Phase 1: Environment & Project Initialization

**Date:** 2026-03-27

**Task:** Set up isolated Python environment using `uv`

**Actions Completed:**
- Initialized `uv` project with Python 3.12
- Added dependencies: `opencv-python`, `opencv-python-headless`, `numpy`, `watchdog`, `pydantic-settings`
- Verified OpenCV installation (version 4.13.0)

**Status:** ✓ Complete

---

### Phase 2: Input Monitoring (The "Hot Folder")

**Date:** 2026-03-27

**Task:** Implement folder watcher for new scan detection

**Actions Completed:**
- Created `watcher.py` with `ImageWatcher` class (FileSystemEventHandler)
- Implemented image extension filtering (.jpg, .png, .tiff)
- Added file readiness check with exponential backoff retry (max 5 attempts, 500ms delay)
- Thread-safe queue management for async processing

**Key Implementation:**
```python
class ImageWatcher(FileSystemEventHandler):
    def _wait_for_file_ready(self, path: str) -> bool:
        # Exponential backoff retry mechanism
        for attempt in range(self.max_retries):
            try:
                with open(path, "rb") as f:
                    f.seek(0, 2)
                return True
            except (IOError, OSError):
                time.sleep(self.retry_delay * (attempt + 1))
        return False
```

**Status:** ✓ Complete

---

### Phase 3: The Vision Pipeline (Detection)

**Date:** 2026-03-27

**Task:** Build document corner detection function

**Actions Completed:**
- Created `detector.py` with `Point` dataclass
- Implemented preprocessing pipeline: resize → gray → Gaussian blur → Otsu threshold
- Added contour extraction with filters:
  - Area filter: 10% - 95% of processed image
  - 4-point check after approxPolyDP
  - Aspect ratio filter: 0.3 - 3.0
- Implemented `_order_points()` for consistent corner ordering (TL, TR, BR, BL)

**Key Implementation:**
```python
def detect_document_corners(image_path: str) -> list[Point] | None:
    # Resize to 640px max for faster processing
    # Otsu thresholding: cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    # Filter contours by area, 4-point check, aspect ratio
    # Return ordered corners in original scale
```

**Tests Passed:**
| Image | Result |
|-------|--------|
| White rect on black | ✓ Detected |
| Skewed document | ✓ Detected |
| Empty (all black) | ✓ Returns None |
| Small document | ✓ Rejected (area too small) |

**Status:** ✓ Complete

---

### Phase 4: Geometry & Perspective Correction

**Date:** 2026-03-27

**Task:** Build perspective warp function

**Actions Completed:**
- Created `warp.py`
- Implemented `_calculate_target_dimensions()` preserving aspect ratio
- Implemented `_rotate_if_needed()` for portrait enforcement (ROTATE_90_CLOCKWISE)
- Used `cv2.getPerspectiveTransform` + `cv2.warpPerspective`

**Key Implementation:**
```python
def warp_document(image: np.ndarray, corners: list[Point]) -> np.ndarray | None:
    # Source: TL, TR, BR, BL (from detect_document_corners)
    # Target: 0,0 → max_width-1,0 → max_width-1,max_height-1 → 0,max_height-1
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(image, matrix, (target_width, target_height))
    return _rotate_if_needed(warped)
```

**Tests Passed:**
| Image | Input | Output |
|-------|-------|--------|
| White on black | 600x800 | 500x600 (portrait) |
| Skewed | Irregular | 443x581 (corrected) |
| Landscape | 800x600 | 500x600 (rotated) |

**Status:** ✓ Complete

---

### Phase 5: Optimization & Output

**Date:** 2026-03-27

**Task:** Build save/export function

**Actions Completed:**
- Created `saver.py`
- Implemented `_resize_if_needed()` with max dimension constraint (2000px default)
- Uses `cv2.INTER_AREA` for downscaling
- Unique filename generation: `{timestamp}_{uuid8}.jpg`
- JPEG quality setting (default 90)
- Auto-creates output folder

**Key Implementation:**
```python
def save_document(image: np.ndarray, output_folder: str, 
                  max_dimension: int = 2000, quality: int = 90) -> str:
    # Only resizes if exceeds max_dimension
    # Uses cv2.INTER_AREA for downscaling
    # Filename: YYYYMMDD_HHMMSS_xxxxxxxx.jpg
```

**Tests Passed:**
| Test | Result |
|------|--------|
| Small image (no resize) | ✓ Preserved |
| Large image (3000x4000) | ✓ Resized to 1500x2000 |
| Quality 95 vs 50 | ✓ 2.8x file size difference |

**Status:** ✓ Complete

---

### Phase 6: Error Handling & Logging

**Date:** 2026-03-27

**Task:** Integrate all components with error handling

**Actions Completed:**
- Created `scanner.py` (main integration)
- Implemented logging to `scanner.log`:
  - `logging.INFO` for success
  - `logging.WARNING` for skipped
  - `logging.ERROR` for failures
- Added upside-down detection and rejection
- Memory cleanup in `finally` block
- Graceful shutdown on Ctrl+C

**Key Implementation:**
```python
def process_image(image_path: str) -> str | None:
    try:
        corners = detect_document_corners(image_path)
        if corners is None:
            _log_skip(image_path, "No document corners detected")
            return None
        # ... warp and save
    finally:
        del image
        del warped
```

**Pipeline Flow:**
```
scans/ → watcher.py → queue.Queue → scanner.py → detector.py → warp.py → saver.py → output/
```

**Status:** ✓ Complete

---

### Portable Windows Deployment

**Date:** 2026-03-27

**Task:** Enable running on Windows without Python or internet

**Actions Completed:**
- Created `portable_scanner/` folder structure
- Added `build_tools/build.bat` (PyInstaller build script)
- Added `run_scanner.bat` (execution script)
- Created `PORTABLE_WINDOWS.md` deployment guide

**Build Process (one-time on Windows with Python):**
```batch
build_tools\build.bat
```

**Status:** ✓ Complete

---

### Documentation

**Date:** 2026-03-27

**Actions Completed:**
- Created `AGENTS.md` for developer/agent instructions
- Created `PORTABLE_WINDOWS.md` for deployment guide
- Updated `README.md` with project overview
- Created `STATUS.md` (this file)

---

### Git Repository

**Date:** 2026-03-27

**Actions Completed:**
- Initialized git repository
- Configured `.gitignore` for Python/uv projects
- Committed all 26 files
- Pushed to GitHub: https://github.com/eurythmia-interactive/python-cv-trim-scanned-image

---

## Test Results Summary

| Component | Test | Result |
|-----------|------|--------|
| Detector | White on black | ✓ |
| Detector | Skewed document | ✓ |
| Detector | Empty image | ✓ |
| Detector | Small document | ✓ (rejected) |
| Warp | Perspective correction | ✓ |
| Warp | Portrait rotation | ✓ |
| Saver | Resize large image | ✓ |
| Saver | Quality settings | ✓ |
| Pipeline | Full integration | ✓ |

---

## Current Status

| Item | Status |
|------|--------|
| Phase 1: Environment | ✓ Complete |
| Phase 2: Watcher | ✓ Complete |
| Phase 3: Detector | ✓ Complete |
| Phase 4: Warp | ✓ Complete |
| Phase 5: Saver | ✓ Complete |
| Phase 6: Integration | ✓ Complete |
| Portable Windows | ✓ Complete |
| Documentation | ✓ Complete |
| Git Repository | ✓ Complete |

**Overall: All tasks complete. Project ready for use.**

---

## Files

| File | Description |
|------|-------------|
| `scanner.py` | Main integration |
| `watcher.py` | Folder monitoring |
| `detector.py` | Corner detection |
| `warp.py` | Perspective correction |
| `saver.py` | Export/save |
| `AGENTS.md` | Developer documentation |
| `PORTABLE_WINDOWS.md` | Windows deployment guide |
| `README.md` | Project overview |
| `STATUS.md` | This file |
| `portable_scanner/` | Portable Windows build |
| `phase_*.md` | Phase documentation |
