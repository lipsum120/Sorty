from pathlib import Path

from app.classes import FileType


TRACKED_FOLDER = "/Users/lipsum/Downloads"
ROOT_FOLDER = Path("/Users/lipsum/Documents/Test")

FILE_TYPES = {
    FileType.IMAGES: {
        "folder": "Images",
        "extensions": [".jpg", ".jpeg", ".png", ".gif"]
    },
    FileType.DOCUMENTS: {
        "folder": "Documents",
        "extensions": [".pdf", ".docx", ".txt"]
    },
    FileType.VIDEOS: {
        "folder": "Videos",
        "extensions": [".mp4", ".mov", ".mkv"]  
    },
    FileType.ARCHIVES: {
        "folder": "Archives",
        "extensions": [".zip", ".rar", ".7z"]
    },
    FileType.OTHERS: {
        "folder": "Others",
        "extensions": []
    }
}

TEMP_EXTENSIONS = {
    ".crdownload",
    ".part",
    ".tmp",
    ".download"
}

