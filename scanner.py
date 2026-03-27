import logging
import argparse
from pathlib import Path

from watcher import ImageWatcher, watch_folder
from detector import detect_document_corners, Point
from warp import warp_document
from saver import save_document


def _setup_logging():
    log_path = Path("scanner.log")
    logging.basicConfig(
        filename=str(log_path),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def _log_success(input_path: str, output_path: str):
    logging.info(f"SUCCESS: {input_path} -> {output_path}")


def _log_failure(input_path: str, reason: str):
    logging.error(f"FAILURE: {input_path} - {reason}")


def _log_skip(input_path: str, reason: str):
    logging.warning(f"SKIPPED: {input_path} - {reason}")


def _check_upside_down(corners: list[Point], image_shape) -> bool:
    img_h, img_w = image_shape[:2]
    tl, tr, br, bl = corners

    top_y_values = [tl.y, tr.y]
    bottom_y_values = [bl.y, br.y]
    avg_top = sum(top_y_values) / len(top_y_values)
    avg_bottom = sum(bottom_y_values) / len(bottom_y_values)

    return avg_bottom < avg_top


def process_image(image_path: str, max_dimension: int, quality: int, output_folder: str) -> str | None:
    image = None
    warped = None
    try:
        corners = detect_document_corners(image_path)
        if corners is None:
            _log_skip(image_path, "No document corners detected")
            return None

        if _check_upside_down(corners, (1, 1)):
            _log_skip(image_path, "Document appears to be upside-down (not supported)")
            return None

        image = __import__('cv2').imread(image_path)
        if image is None:
            _log_failure(image_path, "Failed to read image")
            return None

        warped = warp_document(image, corners)
        if warped is None:
            _log_failure(image_path, "Perspective warp failed")
            return None

        output_path = save_document(warped, output_folder, max_dimension, quality)
        _log_success(image_path, output_path)
        return output_path

    except Exception as e:
        _log_failure(image_path, str(e))
        return None
    finally:
        del image
        del warped


def main():
    parser = argparse.ArgumentParser(description="Document Scanner")
    parser.add_argument("--input", "-i", default="./scans", help="Input folder (default: ./scans)")
    parser.add_argument("--output", "-o", default="./output", help="Output folder (default: ./output)")
    parser.add_argument("--max-size", "-m", type=int, default=2000, help="Max dimension in pixels (default: 2000)")
    parser.add_argument("--quality", "-q", type=int, default=90, help="JPEG quality 1-100 (default: 90)")
    args = parser.parse_args()

    _setup_logging()
    logging.info("Scanner started")
    logging.info(f"Settings: input={args.input}, output={args.output}, max_size={args.max_size}, quality={args.quality}")

    Path(args.output).mkdir(parents=True, exist_ok=True)

    from queue import Queue
    image_queue: Queue = Queue()

    observer = watch_folder(args.input, image_queue)
    logging.info(f"Watching folder: {args.input}")

    try:
        while True:
            try:
                image_path = image_queue.get(timeout=1)
                process_image(image_path, args.max_size, args.quality, args.output)
            except __import__('queue').Empty:
                continue
    except KeyboardInterrupt:
        logging.info("Scanner stopped by user")
    finally:
        observer.stop()
        observer.join()
        logging.info("Scanner shutdown complete")


if __name__ == "__main__":
    main()
