import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


PREPROCESS_MAX_DIM = 640
BLUR_KERNEL = (5, 5)
THRESHOLD_C = 0
APPROX_EPSILON_RATIO = 0.02
MIN_AREA_RATIO = 0.1
MAX_AREA_RATIO = 0.95
ASPECT_RATIO_MIN = 0.3
ASPECT_RATIO_MAX = 3.0


def _resize_image(image: np.ndarray, max_dim: int = PREPROCESS_MAX_DIM) -> tuple[np.ndarray, float]:
    height, width = image.shape[:2]
    scale = 1.0
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return image, scale


def _preprocess(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)
    _, thresh = cv2.threshold(blurred, THRESHOLD_C, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh


def _order_points(pts: np.ndarray) -> list[Point]:
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return [Point(x=p[0], y=p[1]) for p in rect]


def detect_document_corners(image_path: str) -> list[Point] | None:
    image = cv2.imread(image_path)
    if image is None:
        return None

    original_h, original_w = image.shape[:2]
    processed, scale = _resize_image(image)
    processed_h, processed_w = processed.shape[:2]

    thresh = _preprocess(processed)

    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    min_area = (processed_w * processed_h) * MIN_AREA_RATIO
    contours = [c for c in contours if cv2.contourArea(c) > min_area]

    if not contours:
        return None

    max_area = (processed_w * processed_h) * MAX_AREA_RATIO

    rect_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > max_area:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, APPROX_EPSILON_RATIO * peri, True)
        if len(approx) != 4:
            continue
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / h if h > 0 else 0
        if ASPECT_RATIO_MIN <= aspect_ratio <= ASPECT_RATIO_MAX:
            rect_contours.append((area, approx))

    if not rect_contours:
        return None

    _, approx = min(rect_contours, key=lambda x: x[0])
    approx = approx.reshape(4, 2)
    points = _order_points(approx)

    scale_back = 1.0 / scale
    ordered_points = [
        Point(x=p.x * scale_back, y=p.y * scale_back) for p in points
    ]

    return ordered_points


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detector.py <image_path>")
        sys.exit(1)

    corners = detect_document_corners(sys.argv[1])
    if corners:
        print("Document corners detected:")
        for i, corner in enumerate(corners):
            print(f"  {i}: ({corner.x:.1f}, {corner.y:.1f})")
    else:
        print("No document detected")
