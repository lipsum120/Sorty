from pathlib import Path
import logging
import sys
import time

# Allow this file to be launched directly as well as with `python -m app.main`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.folder_tree import FolderNode, FolderTree
from app.utils.build_folder_tree import build_folder_tree, log_folder_tree
from watchdog.observers import Observer
from app.classes import FileTracker
from app.config import ROOT_FOLDER, TRACKED_FOLDER
from app.watcher import DownloadEventHandler
from app.sorter import sorter


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        color = self.COLORS.get(record.levelno, self.RESET)
        return f"{color}{message}{self.RESET}"


handler = logging.StreamHandler()
handler.setFormatter(
    ColorFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler],
)
logger = logging.getLogger(__name__)


def main() -> None:
    tracker = FileTracker()

    observer = Observer()
    observer.schedule(DownloadEventHandler(tracker), TRACKED_FOLDER, recursive=False)
    observer.start()
    logger.info("Started watcher for %s", TRACKED_FOLDER)

    folder_root = FolderNode (
        name = ROOT_FOLDER.name,
        path = ROOT_FOLDER
    )
    build_folder_tree(folder_root)
    folder_tree = FolderTree(folder_root)
    logger.info("Loaded folder tree from %s", folder_tree.root.path)

    log_folder_tree(folder_root)
    logger.info("Watching: %s", TRACKED_FOLDER)
    
    try:
        while True:
            sorter(tracker)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher")
        observer.stop()
    observer.join()
    logger.info("Watcher stopped")


if __name__ == "__main__":
    main()
