# Phase 3: The Vision Pipeline (Detection)

This is where we isolate the white paper from the black table.

## 1. Preprocessing
- **Downscaling:** Create a low-res copy of the image for faster contour detection.
- **Grayscale & Blur:** Convert to gray and apply Gaussian Blur to reduce sensor noise from the scanner.

## 2. Segmentation
- **Thresholding:** Since you have high contrast (White paper vs. Black table), use Otsu's Binarization or a simple binary threshold to create a mask.

## 3. Contour Extraction
- Find all contours in the binary mask.
- Task: Filter contours by area (ignore small dust/noise) and keep the largest rectangular shape.
- Task: Use `approxPolyDP` to simplify the contour into exactly four corner points.

## Task 3
- [x] Build the "Detection" function (Threshold -> Contours -> 4-point detection).
