from app.folder_tree import Node

def build_folder_tree(parent: Node) -> None:
    for item in parent.path.iterdir():
        if item.is_dir():
            child = Node (
                name = item.name, 
                path = item, 
                parent = parent
            )
            parent.children.append(child)
            build_folder_tree(child)
            
def log_folder_tree(root: Node, depth: int = 0) -> None:
    print("  " * depth + root.name)
    for child in root.children:
       log_folder_tree(child, depth + 1)