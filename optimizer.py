import os
import sys
import time
import struct
from pathlib import Path

from core.scanner import scan_images, scan_markdown
from core.converter import convert_image_atomic, is_ffmpeg_available
from core.verifier import verify_webp
from core.rewriter import update_note_references

TARGET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}

def print_banner():
    print(r"""
===================================================================
     ✦ UNIVERSAL IMAGE OPTIMIZER, AUDITOR & LINK REWRITER ✦
===================================================================
  [1] Full Run    : Convert + Verify + Update Markdown Links
  [2] Vault Audit : Scan existing .webp files for corruption (scan_broken_webp)
  [3] Deep Check  : Inspect a single file's RIFF/VP8 chunks (check_image)
===================================================================
""")

def get_input(prompt: str, default: str = "") -> str:
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

# --- MODE 2: AUDIT EXISTING WEBP FILES (From scan_broken_webp.py) ---
def run_vault_audit(vault_path: Path):
    print(f"\n[*] Auditing all existing .webp files in: {vault_path}\n")
    good, broken = 0, []
    
    for root, _, files in os.walk(vault_path):
        for f in files:
            if f.lower().endswith(".webp"):
                p = Path(root) / f
                is_valid, err = verify_webp(p)
                if is_valid:
                    good += 1
                else:
                    rel = p.relative_to(vault_path)
                    broken.append((rel, err))
                    print(f" [CORRUPTED] {rel} -> {err}")

    print("\n" + "=" * 60)
    print(f"Total .webp Scanned : {good + len(broken)}")
    print(f"Healthy             : {good}")
    print(f"Corrupted           : {len(broken)}")
    print("=" * 60)

# --- MODE 3: SINGLE FILE DIAGNOSTIC (From check_image.py) ---
def run_single_check():
    raw_path = get_input("\nEnter full path to the image file to inspect").strip('"')
    p = Path(raw_path)
    if not p.is_file():
        print("❌ File does not exist.")
        return

    with open(p, "rb") as f:
        data = f.read()

    file_size = len(data)
    if file_size < 16 or not data.startswith(b"RIFF") or data[8:12] != b"WEBP":
        print(f"❌ Not a valid WebP container! Header: {data[:12]}")
        return

    riff_size = struct.unpack("<I", data[4:8])[0] + 8
    chunk_type = data[12:16].decode("ascii", errors="replace")

    print(f"\nFile size on disk : {file_size} bytes")
    print(f"Header expects    : {riff_size} bytes")
    print(f"WebP Chunk Type   : {chunk_type}")

    if file_size < riff_size:
        print("❌ Result: File is truncated (incomplete download/compression)!")
    else:
        is_valid, err = verify_webp(p)
        if is_valid:
            print("✅ Result: Bitstream is 100% healthy and decodable!")
        else:
            print(f"❌ Result: Bitstream corruption ({err})")

# --- MODE 1: FULL ATOMIC PIPELINE ---
def run_full_pipeline():
    while True:
        folder_input = get_input("Enter target folder (Obsidian vault or image directory)")
        target_dir = Path(folder_input.strip('"'))
        if target_dir.is_dir():
            break
        print("❌ Directory does not exist.\n")

    ffmpeg_ready = is_ffmpeg_available()
    print("\nSelect Engine:")
    print("  [1] Pillow / libwebp (Zero setup, identical to Caesium) [RECOMMENDED]")
    print("  [2] FFmpeg" + (" (Available)" if ffmpeg_ready else " (Not installed)"))
    engine = "ffmpeg" if get_input("Choice", "1") == "2" and ffmpeg_ready else "pillow"

    print("\nSelect Profile:")
    print("  [1] Extreme Compression (Quality 50) -> 1MB to ~20-30KB")
    print("  [2] Balanced            (Quality 75) [DEFAULT]")
    print("  [3] High Quality        (Quality 85)")
    prof = get_input("Choice", "2")
    quality = 50 if prof == "1" else (85 if prof == "3" else 75)

    dry_run = get_input("\nRun as DRY RUN first? (y/n)", "y").lower() == "y"

    input("\nPress Enter to begin...")
    start_time = time.time()

    images = scan_images(target_dir, TARGET_EXTENSIONS)
    notes = scan_markdown(target_dir)

    print(f"\nFound {len(images)} images and {len(notes)} markdown notes.")
    print("\n--- PHASE 1: COMPRESSION & VERIFICATION ---")
    successful, preserved = 0, 0
    for img in images:
        status, msg = convert_image_atomic(img, quality=quality, engine=engine, dry_run=dry_run)
        rel = img.relative_to(target_dir)
        if status == "OK":
            successful += 1
            print(f" [✓ OPTIMIZED] {rel}")
        elif status == "SKIPPED":
            print(f" [- SKIPPED]   {rel} ({msg})")
        else:
            preserved += 1
            print(f" [✗ PRESERVED] {rel} -> {msg}")

    mod_notes, mod_links = 0, 0
    if notes:
        print("\n--- PHASE 2: LINK UPDATES ---")
        mod_notes, mod_links = update_note_references(notes, TARGET_EXTENSIONS, target_dir, dry_run)

    print("\n" + "=" * 60)
    print(f"Finished in {round(time.time() - start_time, 2)}s")
    print(f"Images Converted : {successful} | Failed/Preserved: {preserved}")
    print(f"Notes Modified   : {mod_notes} | Links Updated: {mod_links}")
    if dry_run:
        print(" * DRY RUN ONLY. Run again with 'n' to write to disk. *")
    print("=" * 60)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()
    print("What would you like to do?")
    print("  [1] Optimize images & rewrite links (Full Pipeline)")
    print("  [2] Audit existing .webp images for corruption")
    print("  [3] Deep inspect a single image file")
    
    choice = get_input("\nSelect an option (1-3)", "1")
    if choice == "2":
        path_input = get_input("Enter folder to audit").strip('"')
        run_vault_audit(Path(path_input))
    elif choice == "3":
        run_single_check()
    else:
        run_full_pipeline()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Exited safely.")
        sys.exit(0)