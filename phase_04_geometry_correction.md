# Phase 4: Geometry & Perspective Correction

Even if the paper is slightly crooked on the scanner, we want it perfectly square and portrait.

## 1. Corner Sorting
- Identify which of the four points is Top-Left, Top-Right, Bottom-Left, and Bottom-Right.

## 2. Perspective Warp
- Calculate the "Target Dimensions." (e.g., if the paper is roughly A4, define a target aspect ratio).
- Use `cv2.getPerspectiveTransform` and `cv2.warpPerspective` to "flatten" the drawing, effectively removing any skew and the surrounding black table.

## 3. Orientation Enforcement
- Task: Check the final width vs. height. If `width > height`, rotate the image 90 degrees to force a **Portrait** orientation.

## Task 4
- [x] Build the "Warp" function (Perspective Transform + Rotation logic).
