# Phase 5: Optimization & Output

Turning the raw processed data into a web/projection-ready file.

## 1. Resizing Logic
- Implement a "Max Dimension" constraint (e.g., 2000px height). Resize the image using `cv2.INTER_AREA` (best for downscaling) while maintaining the aspect ratio.

## 2. Color Correction (Optional)
- Apply a slight brightness/contrast boost to "whiten" the paper background if the scan appears grey.

## 3. Export Strategy
- Save to the "Output" folder using a unique naming convention (Timestamp or UUID).
- Set the JPEG compression quality (typically 85-90) to balance file size and visual fidelity for the projector.

## Task 5
- [x] Build the "Save" function (Resize + JPG export).
