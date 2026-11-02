from pathlib import Path
from PIL import Image

def verify_webp(file_path: Path) -> tuple[bool, str]:
    """
    Performs a deep 2-stage verification on a WebP file:
    1. Header/container structure check (img.verify)
    2. Full bitstream pixel decompression (img.load)
    Returns: (is_valid: bool, error_message: str)
    """
    try:
        # Stage 1: Container verification
        with Image.open(file_path) as img:
            img.verify()

        # Stage 2: Force complete pixel payload decoding
        # (Catches VP8/VP8X bitstream corruption that breaks Obsidian/Chrome)
        with Image.open(file_path) as img:
            img.load()

        return True, ""
    except Exception as e:
        return False, str(e)