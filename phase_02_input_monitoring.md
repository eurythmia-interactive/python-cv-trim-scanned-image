# Phase 2: Input Monitoring (The "Hot Folder")

Since scanners often write files in chunks, we need a robust way to detect when a file is **finished** writing.

## 1. Watcher Setup
- Implement a `FileSystemEventHandler` using the `watchdog` library.
- Filter specifically for image extensions (`.jpg`, `.png`, `.tiff`).

## 2. The "Atomic Write" Problem
- Task: Create a retry mechanism or a small delay (e.g., 500ms) after a file is detected to ensure the scanner has closed the file handle before Python tries to open it.

## 3. Queue Management
- Implement a thread-safe queue to process images one by one, ensuring the scanner can keep working even if the processing takes a moment.

## Task 2
- [x] Write the folder watcher script that prints "New Image Detected" when a file is saved.
