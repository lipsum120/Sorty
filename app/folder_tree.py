from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FolderNode:
    name: str
    path: Path
    parent: FolderNode | None = None
    children: list[FolderNode] = field(default_factory=list)
    
@dataclass
class FolderTree:
    root: FolderNode