import time
import queue
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}


class ImageWatcher(FileSystemEventHandler):
    def __init__(self, image_queue: queue.Queue, max_retries: int = 5, retry_delay: float = 0.5):
        self.image_queue = image_queue
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        super().__init__()

    def _is_image_file(self, path: str) -> bool:
        return Path(path).suffix.lower() in IMAGE_EXTENSIONS

    def _wait_for_file_ready(self, path: str) -> bool:
        for attempt in range(self.max_retries):
            try:
                with open(path, "rb") as f:
                    f.seek(0, 2)
                return True
            except (IOError, OSError):
                time.sleep(self.retry_delay * (attempt + 1))
        return False

    def on_created(self, event):
        if event.is_directory:
            return
        if not self._is_image_file(event.src_path):
            return
        if self._wait_for_file_ready(event.src_path):
            self.image_queue.put(event.src_path)
            print(f"New Image Detected: {event.src_path}")
        else:
            print(f"Failed to read file after {self.max_retries} attempts: {event.src_path}")


def watch_folder(folder_path: str, image_queue: queue.Queue):
    event_handler = ImageWatcher(image_queue)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    return observer


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python watcher.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    if not Path(folder).exists():
        print(f"Folder does not exist: {folder}")
        sys.exit(1)

    image_queue: queue.Queue = queue.Queue()
    observer = watch_folder(folder, image_queue)

    print(f"Watching folder: {folder}")
    print("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
