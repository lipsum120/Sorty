from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
import time

class FileStatus(StrEnum):
    DOWNLOADING = "downloading"
    READY = "ready"
    SORTED = "sorted"
    FAILED = "failed"
    
class FileType(StrEnum):
    IMAGES = "Images"
    DOCUMENTS = "Documents"
    VIDEOS = "Videos"
    ARCHIVES = "Archives"
    OTHERS = "Others"

@dataclass
class TrackedFile:
    path: Path = Path("")
    last_event_time: float = 0
    last_size: int = 0
    status: FileStatus = FileStatus.DOWNLOADING
    file_type: FileType = FileType.OTHERS

    def is_stable(self) -> bool:
        return time.monotonic() - self.last_event_time >= 2
        
    def set_status(self, status: FileStatus) -> None:
        self.status = status
        
    def set_file_type(self, file_type: FileType) -> None:
        self.file_type = file_type
        
    def update_path(self, new_path: Path) -> None:
        self.path = new_path
    
    def update_last_event_time(self) -> None:
        self.last_event_time = time.monotonic()
        
    def update_last_size(self) -> None:
        self.last_size = self.path.stat().st_size


@dataclass
class FileTracker:
    tracked_files: dict[Path, TrackedFile] = field(default_factory=dict)

    def get_file(self, path: Path) -> TrackedFile | None:
        return self.tracked_files.get(path)

    def add_file(self, file: TrackedFile) -> None:
        self.tracked_files[file.path] = file

    def remove_file(self, path: Path) -> None:
        self.tracked_files.pop(path, None)
