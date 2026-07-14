from pathlib import Path
import sys
import time

# Allow this file to be launched directly as well as with `python -m app.main`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.folder_tree import Node, Tree
from app.utils.init_folder_struct import build_folder_tree, log_folder_tree
from watchdog.observers import Observer
from app.classes import FileTracker
from app.config import ROOT_FOLDER, TRACKED_FOLDER
from app.watcher import DownloadEventHandler
from app.sorter import sorter


def main() -> None:
    tracker = FileTracker()

    observer = Observer()
    observer.schedule(DownloadEventHandler(tracker), TRACKED_FOLDER, recursive=False)
    observer.start()

    folder_root = Node (
        name = Path(ROOT_FOLDER).name,
        path = Path(ROOT_FOLDER)
    )
    
    build_folder_tree(folder_root)
    folder_tree = Tree(folder_root)

    log_folder_tree(folder_root)
    
    print("Watching:", TRACKED_FOLDER)
    

    try:
        while True:
            sorter(tracker)
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
