from pathlib import Path
import logging
import time
from watchdog.events import FileSystemEventHandler
from app.classes import TrackedFile, FileStatus, FileTracker
from app.utils import get_file_type, is_temporary


logger = logging.getLogger(__name__)


class DownloadEventHandler (FileSystemEventHandler):
    def __init__ (self, tracker):
        self.tracker: FileTracker = tracker

    def on_any_event(self, event) -> None:
        path: Path = Path(event.src_path)
        file: TrackedFile | None = self.tracker.get_file(path)
        

        if event.event_type == "deleted" and file is not None:
            self.tracker.remove_file(file.path)
            logger.info("Removed deleted file from tracker: %s", file.path)
            return

        if is_temporary(path) or path.is_dir() or not path.exists():
            logger.debug("Ignored event=%s path=%s", event.event_type, path)
            return

        try:
            if file is None:
                file_type = get_file_type(path)
                file = TrackedFile(
                    path,
                    time.monotonic(),
                    path.stat().st_size,
                    FileStatus.DOWNLOADING,
                    file_type
                )
                self.tracker.add_file(file)
                logger.info("Started tracking file: %s type=%s", path, file_type.value)
            else:
                file.update_last_event_time()
                file.update_last_size()
                logger.debug("Updated tracked file: %s size=%s", file.path, file.last_size)
            file.status = FileStatus.DOWNLOADING
        except FileNotFoundError:
            logger.debug("File disappeared before it could be tracked: %s", path)
            return
