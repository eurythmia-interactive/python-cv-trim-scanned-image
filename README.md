# Document Scanner

Automated document scanning pipeline using OpenCV. Monitors a folder for scanned images, detects document boundaries, corrects perspective, and outputs cropped images ready for projection.

## Features

- **Automatic detection** - Detects white paper on dark background using contour analysis
- **Perspective correction** - Flattens skewed documents using `cv2.warpPerspective`
- **Portrait enforcement** - Automatically rotates landscape images to portrait
- **Hot folder monitoring** - Watches for new scans and processes them automatically
- **Portable deployment** - Standalone Windows executable (no Python required)

## Quick Start

### Run with uv

```bash
uv sync
uv run python scanner.py
```

### Test individual components

```bash
uv run python detector.py <image>     # Detect document corners
uv run python warp.py <image>          # Apply perspective correction
uv run python saver.py <image> <output> # Save with resize
```

## Project Structure

```
.
├── scanner.py      # Main integration (watcher → detect → warp → save)
├── watcher.py      # File system monitoring
├── detector.py     # Document corner detection
├── warp.py         # Perspective correction
├── saver.py        # Resize and JPEG export
└── output/         # Processed images
```

## How It Works

1. Place scanned images (`.jpg`, `.png`, `.tiff`) in the `scans/` folder
2. The scanner detects document boundaries using OpenCV contour analysis
3. Perspective is corrected and images are rotated to portrait orientation
4. Processed images are saved to `output/` with timestamps

## Requirements

- Python 3.12+
- opencv-python
- numpy
- watchdog

## Portable Windows Build

See [PORTABLE_WINDOWS.md](PORTABLE_WINDOWS.md) for instructions to build a standalone `.exe` for Windows with no Python installation required.

## License

MIT
