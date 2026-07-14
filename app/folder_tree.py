from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Node:
    name: str
    path: Path
    parent: Node | None = None
    children: list[Node] = field(default_factory=list)
    
@dataclass
class Tree:
    root: Node