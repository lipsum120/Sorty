from pathlib import Path
import logging

from app.classes import FileType
from app.config import FILE_TYPES, TEMP_EXTENSIONS


logger = logging.getLogger(__name__)


def is_temporary(path: Path) -> bool:
    return path.name.startswith(".") or path.suffix.lower() in TEMP_EXTENSIONS

def get_file_type(path: Path) -> FileType:
    extension = path.suffix.lower()
    
    for file_type, config in FILE_TYPES.items():
        if extension in config["extensions"]:
            logger.debug("Detected file type: %s -> %s", path, file_type.value)
            return file_type
        
    logger.debug("Using fallback file type: %s -> %s", path, FileType.OTHERS.value)
    return FileType.OTHERS
