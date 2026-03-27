# Agent Instructions for Python-CV-trim-Scanned-Image

Document scanner pipeline using OpenCV for computer vision. Monitors a folder for scanned images, detects document boundaries, corrects perspective, and outputs cropped images.

## Project Overview

```
scanner.py       # Main integration (watcher → detect → warp → save)
watcher.py       # File system monitoring for new scans
detector.py      # Document corner detection via contour analysis
warp.py          # Perspective correction and portrait rotation
saver.py         # Resize and JPEG export with quality settings
```

## Build & Run Commands

### Package Management (uv)
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package>

# Run any script with venv activated
uv run python <script.py>

# Run with specific Python version
uv run --python 3.12 python <script.py>
```

### Testing Individual Components
```bash
# Test document detection
uv run python detector.py <image_path>

# Test perspective warp
uv run python warp.py <image_path>

# Test save/export
uv run python saver.py <image_path> <output_folder>

# Test folder watcher
uv run python watcher.py <folder_path>

# Test full pipeline
uv run python scanner.py
```

### Manual Pipeline Testing
```bash
# Create test image (white rect on black)
uv run python -c "
import cv2, numpy as np
img = np.zeros((800, 600, 3), dtype=np.uint8)
cv2.rectangle(img, (50, 100), (550, 700), (255, 255, 255), -1)
cv2.imwrite('test.jpg', img)
"

# Run detector
uv run python detector.py test.jpg

# Run full pipeline manually
uv run python -c "
from detector import detect_document_corners
from warp import warp_document
from saver import save_document
import cv2

corners = detect_document_corners('test.jpg')
if corners:
    img = cv2.imread('test.jpg')
    warped = warp_document(img, corners)
    if warped is not None:
        path = save_document(warped, 'output')
        print(f'Saved: {path}')
"
```

## Code Style Guidelines

### Type Hints
- Use Python 3.12+ syntax: `list[Point]`, `dict[str, Any]`
- Return types required on public functions: `def func() -> list[Point] | None:`
- Use `np.ndarray` for images, `list[Point]` for corner lists

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Modules | snake_case | `scanner.py`, `my_module.py` |
| Classes | PascalCase | `ImageWatcher`, `Point` |
| Public Functions | snake_case | `detect_document_corners()` |
| Private Functions | _prefixed | `_resize_image()`, `_order_points()` |
| Constants | UPPER_SNAKE | `MAX_DIMENSION`, `BLUR_KERNEL` |
| Variables | snake_case | `image_queue`, `target_width` |

### Imports (Standard Order)
1. Standard library
2. Third-party (cv2, numpy, watchdog, etc.)
3. Local imports

```python
# Standard
import logging
from pathlib import Path
from datetime import datetime
from queue import Queue

# Third-party
import cv2
import numpy as np
from watchdog.events import FileSystemEventHandler

# Local
from detector import Point, detect_document_corners
```

### Dataclasses
Use `@dataclass` for simple data containers:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

### Error Handling
- Return `None` on failure for nullable returns (detector, warp)
- Raise exceptions only for truly unexpected conditions
- Log all failures with context in `scanner.py`:
```python
_log_failure(input_path, "Reason: details")
_log_skip(input_path, "Reason: condition not met")
```
- Always clean up resources in `finally` block:
```python
finally:
    del image
    del warped
```

### OpenCV Conventions
- Images are BGR `np.ndarray` (height, width, channels)
- Use `cv2.INTER_AREA` for downscaling
- Use `cv2.ROTATE_90_CLOCKWISE` for portrait enforcement
- Threshold flags: `cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU`
- Contour retrieval: `cv2.RETR_LIST`, approximation: `cv2.CHAIN_APPROX_SIMPLE`

### Geometry Conventions
- Corners ordered: TL, TR, BR, BL (via `_order_points()`)
- Point coordinates: `(x, y)` where x is horizontal, y is vertical
- Scale factor: original_dimension / processed_dimension
- Target dimensions: preserve source aspect ratio

### Logging
```python
logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("SUCCESS: {input} -> {output}")
logging.error("FAILURE: {path} - {reason}")
logging.warning("SKIPPED: {path} - {reason}")
```

### Magic Numbers (Avoid)
Use named constants:
```python
# Bad
if width > 2000:

# Good
MAX_DIMENSION = 2000
if width > MAX_DIMENSION:
```

## Architecture Notes

### Pipeline Flow
```
scans/ folder → watcher.py (detects new file)
                        ↓
              queue.Queue (thread-safe)
                        ↓
              scanner.py (process_image)
                        ↓
              detector.py (returns list[Point] or None)
                        ↓
              warp.py (returns warped image or None)
                        ↓
              saver.py (returns output path)
                        ↓
              output/ folder
```

### File Readiness Problem
Scanners write files incrementally. `watcher.py` uses:
- Exponential backoff retry (500ms * attempt)
- Max 5 attempts
- File handle check via `f.seek(0, 2)`

### Document Detection Filters
1. Area filter: 10% - 95% of processed image
2. Shape filter: exactly 4 points after approxPolyDP
3. Aspect ratio filter: 0.3 - 3.0 (rejects thin strips, accepts A4-ish)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "No document detected" | Check if image is white-on-black contrast |
| "Upside-down rejected" | Flip document before scanning |
| "File in use" | Increase retry_delay in ImageWatcher |
| Empty output | Verify input folder path is correct |

## Testing Tips

```bash
# Test with debug prints
uv run python -c "
import cv2, numpy as np
# Create known test image
img = np.zeros((800, 600, 3), dtype=np.uint8)
cv2.rectangle(img, (50, 100), (550, 700), (255, 255, 255), -1)
cv2.imwrite('/tmp/test.jpg', img)
"

# Verify intermediate steps
uv run python -c "
import cv2
img = cv2.imread('/tmp/test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('/tmp/gray.jpg', gray)
"
```
