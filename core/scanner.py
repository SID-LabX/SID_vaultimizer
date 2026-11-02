import os
from pathlib import Path

IGNORED_DIRS = {".obsidian", ".trash", ".git", ".venv", "__pycache__", "node_modules"}

def scan_images(vault_path: Path, target_extensions: set[str]) -> list[Path]:
    """Finds all image files matching target extensions across all nested folders."""
    found_images = []
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            p = Path(root) / file
            if p.suffix.lower() in target_extensions:
                found_images.append(p)
    return found_images

def scan_markdown(vault_path: Path) -> list[Path]:
    """Finds all .md files across all nested folders."""
    found_notes = []
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            if file.lower().endswith(".md"):
                found_notes.append(Path(root) / file)
    return found_notes