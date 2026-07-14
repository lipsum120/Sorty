from pathlib import Path
import time
from watchdog.events import FileSystemEventHandler
from app.classes import File, FileStatus, FileTracker
from app.utils import get_file_type, is_temporary

class DownloadEventHandler (FileSystemEventHandler):
    def __init__ (self, tracker):
        self.tracker: FileTracker = tracker

    def on_any_event(self, event) -> None:
        path: Path = Path(event.src_path)
        file: File = self.tracker.get_file(path)
        

        if event.event_type == "deleted" and file is not None:
            self.tracker.remove_file(file.path)
            return

        if is_temporary(path) or path.is_dir() or not path.exists():
            return

        try:
            if file is None:
                file = File(
                    path,
                    time.monotonic(),
                    path.stat().st_size,
                    FileStatus.DOWNLOADING,
                    get_file_type(path)
                )
                self.tracker.add_file(file)
            else:
                file.update_last_event_time()
                file.update_last_size()
            file.status = FileStatus.DOWNLOADING
        except FileNotFoundError:
            return
