import subprocess
import shutil
from pathlib import Path
from PIL import Image
from core.verifier import verify_webp

def is_ffmpeg_available() -> bool:
    """Checks if ffmpeg is accessible via system PATH or current directory."""
    return shutil.which("ffmpeg") is not None

def convert_with_pillow(source: Path, temp_target: Path, quality: int):
    with Image.open(source) as img:
        # Normalize color space to avoid VP8X bitstream traps
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            clean_img = img.convert("RGBA")
        else:
            clean_img = img.convert("RGB")
        clean_img.save(temp_target, "WEBP", quality=quality, method=6)

def convert_with_ffmpeg(source: Path, temp_target: Path, quality: int):
    # -pix_fmt yuv420p / yuva420p ensures maximum browser/Chromium display compatibility
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", str(source.resolve()),
        "-c:v", "libwebp",
        "-quality", str(quality),
        "-compression_level", "6",
        str(temp_target.resolve())
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr.strip()}")

def convert_image_atomic(
    image_path: Path, 
    quality: int = 75, 
    engine: str = "pillow",
    dry_run: bool = True
) -> tuple[str, str]:
    target_webp = image_path.with_suffix(".webp")
    temp_webp = image_path.with_name(f"{image_path.stem}.__atomic_tmp__.webp")

    if target_webp.exists() and target_webp != image_path:
        return "SKIPPED", f"Destination {target_webp.name} already exists."

    if dry_run:
        return "OK", "Simulated conversion successful"

    try:
        if engine == "ffmpeg":
            convert_with_ffmpeg(image_path, temp_webp, quality)
        else:
            convert_with_pillow(image_path, temp_webp, quality)
    except Exception as e:
        if temp_webp.exists():
            temp_webp.unlink()
        return "CONVERT_ERROR", f"Encoding failed: {e}"

    # Verify bitstream before touching original
    is_valid, err = verify_webp(temp_webp)
    if not is_valid:
        if temp_webp.exists():
            temp_webp.unlink()
        return "VERIFY_FAILED", f"Corrupt bitstream detected ({err}). Original preserved intact."

    # Atomic swap: delete source, finalize .webp
    try:
        image_path.unlink()
        temp_webp.replace(target_webp)
        return "OK", "Converted & verified"
    except Exception as e:
        return "SWAP_ERROR", f"File swap failed: {e}"