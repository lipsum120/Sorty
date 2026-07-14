from pathlib import Path

from app.classes import FileType
from app.config import FOLDER_STRUCTURE, TEMP_EXTENSIONS

def is_temporary(path: Path) -> bool:
    return path.name.startswith(".") or path.suffix.lower() in TEMP_EXTENSIONS

def get_file_type(path: Path) -> FileType:
    extension = path.suffix.lower()
    
    for file_type, config in FOLDER_STRUCTURE.items():
        if extension in config["format"]:
            return FileType(file_type)
        
    return FileType.OTHERS