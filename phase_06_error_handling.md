# Phase 6: Error Handling & Logging

Ensuring the installation can run for hours without crashing.

## 1. Edge Case Handling
- What if the scanner is triggered with no paper? (Logic to ignore images where no large contour is found).
- What if the drawing is placed upside down? (Optional: Use OpenCV to detect the "heaviness" of the drawing to guess orientation).

## 2. System Logging
- Log every successful process and every error to a text file for troubleshooting.

## 3. Resource Cleanup
- Ensure memory is cleared after each image is processed to prevent leaks during long-running installations.

## Task 6
- [x] Integrate all components into a single loop.
