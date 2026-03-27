# Phase 1: Environment & Project Initialization

In this phase, we establish an isolated, high-performance Python environment using `uv`.

## 1. Project Creation
- Initialize a new project using `uv init`.
- Configure the project to use a specific Python version (e.g., 3.12) to ensure stability.

## 2. Dependency Specification
- Add `opencv-python`: The core vision library.
- Add `numpy`: For high-speed matrix operations on image data.
- Add `watchdog`: To monitor the file system for new scans in real-time.
- Add `pydantic-settings`: (Optional but recommended) To manage folder paths and parameters via a config file or environment variables.

## 3. Environment Sync
- Run `uv sync` to generate the lockfile and install all dependencies into a `.venv` folder.

## Task 1
- [ ] Initialize `uv` project and install `opencv-python`, `numpy`, and `watchdog`.
