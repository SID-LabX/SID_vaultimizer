import re
from pathlib import Path

def update_note_references(
    note_paths: list[Path],
    target_extensions: set[str],
    vault_path: Path,
    dry_run: bool = True
) -> tuple[int, int]:
    """
    Scans notes and replaces image extensions with .webp.
    Skips external URLs (https://... or http://...).
    Returns: (modified_notes_count, total_links_changed)
    """
    ext_pattern = "|".join([ext.lstrip(".") for ext in target_extensions])
    combined_regex = re.compile(
        rf'(https?://[^\s\)\]\"\'\>]+)|(\.(?:{ext_pattern})(?=[\]\)\>\"\'\s|#\^|;]|$))',
        re.IGNORECASE
    )

    modified_notes = 0
    total_links_changed = 0

    for md_path in note_paths:
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(md_path, "r", encoding="utf-8-sig", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                print(f" [!] Could not read: {md_path.name} ({e})")
                continue

        changes = 0
        def replacer(match):
            nonlocal changes
            # If group 1 matched, it's an external web URL -> keep as-is
            if match.group(1):
                return match.group(1)
            changes += 1
            return ".webp"

        new_content = combined_regex.sub(replacer, content)

        if changes > 0:
            modified_notes += 1
            total_links_changed += changes
            rel_path = md_path.relative_to(vault_path)
            print(f" [NOTE UPDATED] {rel_path} -> {changes} reference(s)")

            if not dry_run:
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

    return modified_notes, total_links_changed