import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
import uuid


DEFAULT_MAX_DIMENSION = 2000
DEFAULT_QUALITY = 90


def _resize_if_needed(image: np.ndarray, max_dimension: int) -> np.ndarray:
    height, width = image.shape[:2]
    if height <= max_dimension and width <= max_dimension:
        return image

    scale = max_dimension / max(height, width)
    new_width = int(width * scale)
    new_height = int(height * scale)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


def _generate_filename() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.jpg"


def save_document(
    image: np.ndarray,
    output_folder: str,
    max_dimension: int = DEFAULT_MAX_DIMENSION,
    quality: int = DEFAULT_QUALITY
) -> str:
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    resized = _resize_if_needed(image, max_dimension)

    filename = _generate_filename()
    filepath = output_path / filename

    cv2.imwrite(str(filepath), resized, [cv2.IMWRITE_JPEG_QUALITY, quality])

    return str(filepath)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python saver.py <image_path> <output_folder>")
        sys.exit(1)

    image = cv2.imread(sys.argv[1])
    if image is None:
        print(f"Failed to read image: {sys.argv[1]}")
        sys.exit(1)

    output_path = save_document(image, sys.argv[2])
    print(f"Saved: {output_path}")
    img_check = cv2.imread(output_path)
    print(f"Size: {img_check.shape[1]}x{img_check.shape[0]}")
