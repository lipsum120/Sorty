from pathlib import Path

from app.classes import FileStatus, FileTracker
from app.config import FOLDER_STRUCTURE
from app.utils import move_file


def sorter(tracker: FileTracker):
    for file in list(tracker.tracked_files.values()):
        if file.is_stable():
            try:
                old_path = file.path
                move_file(file, Path(FOLDER_STRUCTURE[file.file_type.value]["path"]))
                tracker.remove_file(old_path)
            except Exception as e:
                print(e)
                file.set_status(FileStatus.FAILED)