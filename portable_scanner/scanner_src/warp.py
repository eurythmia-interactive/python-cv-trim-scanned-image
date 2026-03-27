import cv2
import numpy as np
from detector import Point


def _calculate_target_dimensions(corners: list[Point]) -> tuple[int, int]:
    tl, tr, br, _ = corners

    width_top = np.sqrt((tr.x - tl.x) ** 2 + (tr.y - tl.y) ** 2)
    width_bottom = np.sqrt((br.x - corners[2].x) ** 2 + (br.y - corners[2].y) ** 2)
    max_width = max(width_top, width_bottom)

    height_left = np.sqrt((tl.x - corners[3].x) ** 2 + (tl.y - corners[3].y) ** 2)
    height_right = np.sqrt((tr.x - corners[2].x) ** 2 + (tr.y - corners[2].y) ** 2)
    max_height = max(height_left, height_right)

    return int(max_width), int(max_height)


def _rotate_if_needed(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    if width > height:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image


def warp_document(image: np.ndarray, corners: list[Point]) -> np.ndarray | None:
    if len(corners) != 4:
        return None

    src_pts = np.array([
        [corners[0].x, corners[0].y],
        [corners[1].x, corners[1].y],
        [corners[2].x, corners[2].y],
        [corners[3].x, corners[3].y]
    ], dtype=np.float32)

    target_width, target_height = _calculate_target_dimensions(corners)

    if target_width < 10 or target_height < 10:
        return None

    dst_pts = np.array([
        [0, 0],
        [target_width - 1, 0],
        [target_width - 1, target_height - 1],
        [0, target_height - 1]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(image, matrix, (target_width, target_height))

    rotated = _rotate_if_needed(warped)

    return rotated


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python warp.py <image_path>")
        sys.exit(1)

    from detector import detect_document_corners

    corners = detect_document_corners(sys.argv[1])
    if corners is None:
        print("No document detected")
        sys.exit(1)

    image = cv2.imread(sys.argv[1])
    result = warp_document(image, corners)

    if result is not None:
        output_path = sys.argv[1].rsplit(".", 1)[0] + "_warped.jpg"
        cv2.imwrite(output_path, result)
        print(f"Saved: {output_path}")
        print(f"Output size: {result.shape[1]}x{result.shape[0]}")
    else:
        print("Warp failed")
