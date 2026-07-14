from pathlib import Path
import shutil

from app.classes import File


def move_file(file: File, dest: Path) -> None:
        dest.mkdir(parents=True, exist_ok=True) # create folder if dont exsits
        new_path: Path = dest / file.path.name
        count: int = 1
        
        while new_path.exists():
            new_path = dest / (file.path.stem + f" ({count})" + file.path.suffix)
            count += 1
            
        try:
            shutil.move(file.path, new_path)
        except FileNotFoundError:
            return

        file.update_path(new_path)