from pathlib import Path
import logging
import shutil

from app.classes import TrackedFile


logger = logging.getLogger(__name__)


def move_file(file: TrackedFile, dest: Path) -> None:
        dest.mkdir(parents=True, exist_ok=True) # create folder if dont exsits
        new_path: Path = dest / file.path.name
        count: int = 1
        
        while new_path.exists():
            new_path = dest / (file.path.stem + f" ({count})" + file.path.suffix)
            count += 1
        if new_path.name != file.path.name:
            logger.info("Resolved duplicate filename: %s -> %s", file.path.name, new_path.name)
            
        try:
            shutil.move(file.path, new_path)
        except FileNotFoundError:
            logger.warning("File was missing before move: %s", file.path)
            return

        logger.info("Moved file on disk: %s -> %s", file.path, new_path)
        file.update_path(new_path)
