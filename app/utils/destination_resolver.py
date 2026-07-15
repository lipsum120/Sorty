from pathlib import Path
import logging

from app.classes import FileType
from app.config import FILE_TYPES, ROOT_FOLDER


logger = logging.getLogger(__name__)


def destination_resolver(file_type: FileType) -> Path: 
    destination = ROOT_FOLDER / Path(FILE_TYPES[file_type]["folder"])
    logger.debug("Resolved destination for %s: %s", file_type.value, destination)
    return destination
