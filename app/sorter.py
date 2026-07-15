import logging

from app.classes import FileStatus, FileTracker
from app.utils import destination_resolver, move_file


logger = logging.getLogger(__name__)


def sorter(tracker: FileTracker):
    for file in list(tracker.tracked_files.values()):
        if file.is_stable():
            try:
                old_path = file.path
                destination = destination_resolver(file.file_type)
                logger.info("File is stable, moving: %s -> %s", old_path, destination)
                move_file(file, destination)
                file.set_status(FileStatus.SORTED)
                tracker.remove_file(old_path)
                logger.info("Sorted file: %s -> %s", old_path, file.path)
            except Exception as e:
                file.set_status(FileStatus.FAILED)
                logger.exception("Failed to sort file: %s", file.path)
