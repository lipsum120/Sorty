import logging

from app.folder_tree import FolderNode


logger = logging.getLogger(__name__)


def build_folder_tree(parent: FolderNode) -> None:
    for item in parent.path.iterdir():
        if item.is_dir():
            child = FolderNode (
                name = item.name, 
                path = item, 
                parent = parent
            )
            parent.children.append(child)
            logger.debug("Added folder tree node: %s", item)
            build_folder_tree(child)
            
def log_folder_tree(root: FolderNode, depth: int = 0) -> None:
    print("  " * depth + root.name)
    for child in root.children:
       log_folder_tree(child, depth + 1)
