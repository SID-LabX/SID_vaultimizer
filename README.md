# SID_vaultimizer

A brief description of what this project does.

## Contributing

We welcome contributions! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and note that all contributors must sign our [Contributor License Agreement (CLA)](CLA.md) before pull requests can be merged.

## License

This project is licensed under the terms of the [PROPRIETARY SOURCE-AVAILABLE LICENSE](LICENSE).

---

# ✦ Universal Vault Image Optimizer & Link Rewriter

An atomic, fail-safe image compressor and link rewriter designed for Obsidian vaults and deep folder hierarchies. 

It converts all `.png`, `.jpg`, `.jpeg`, `.bmp`, and `.tiff` images into web-standard `.webp`, automatically verifies their pixel bitstreams before touching the originals, and rewrites all markdown notes (frontmatter and body) to point to the new `.webp` files.

---

## ⚡ Quick Start on a Fresh PC (Zero Setup Required)

You do **not** need to manually configure environments, pip commands, or terminal paths. The launcher does everything automatically.

### 1. Requirements
* Windows 10 or 11.
* [Python 3.10+](https://www.python.org/downloads/) installed.  
  ⚠️ **Important:** During Python installation, make sure to check the box that says **"Add Python to PATH"**.

### 2. How to Run
1. Double-click **`run.bat`**.
2. The script will automatically:
   - Create an isolated virtual environment (`.venv`).
   - Install required dependencies silently.
   - Start the interactive program.
3. Paste the path to your folder (or drag and drop the folder directly into the window).
4. Choose your compression level:
   - **Extreme Compression (Quality 50):** Turns 1 MB images into ~20–30 KB.
   - **Balanced (Quality 75):** Recommended for crystal-clear text & photos.
5. Keep **DRY RUN = y** on your first pass to preview the changes.
6. When satisfied, run it again with **DRY RUN = n** to apply the changes.

---

## 🛡️ Fail-Safe "Atomic" Architecture

Standard batch compressors often corrupt complex color spaces (e.g. CMYK JPEGs or indexed PNGs), resulting in images that refuse to render in Obsidian or Google Chrome. 

This tool prevents corruption through a **4-step atomic pipeline**:
1. **Color Normalization:** Normalizes color spaces to standard sRGB/RGBA to prevent broken WebP `VP8X` chunks.
2. **Buffer Output:** Encodes to an isolated temporary file (`.__atomic_tmp__.webp`).
3. **Full Bitstream Verification:** Forces a complete in-memory pixel decompression pass (`img.verify()` and `img.load()`).
4. **Guaranteed Zero-Loss Swap:** The original file is **only deleted after the new WebP is 100% verified as healthy**. If an image fails verification, the original remains untouched.

---

## ❓ Frequently Asked Questions

#### Can this compress a 1 MB file into 20 KB like Caesium?
**Yes.** Caesium, FFmpeg, and Pillow all use Google's official C library (`libwebp`). Selecting **Profile [1] (Extreme Compression)** applies maximum compression effort (`method 6`), reducing high-resolution images down to 20–40 KB with negligible visual loss.

#### Does this work on folders other than Obsidian?
**Yes.** You can point it at any folder (photo libraries, project assets, downloads). If there are no markdown files in the folder, it simply optimizes the images and skips Phase 2.

#### Will it break my external web links?
**No.** Any URLs starting with `http://` or `https://` (such as OpenLibrary covers) are protected by the regex parser and will not be altered.

#### How do I use FFmpeg instead of the built-in engine?
If you have `ffmpeg.exe` installed and added to your system PATH, the menu will automatically detect it and let you select **[2] FFmpeg** as the backend.

---

## 📂 Project Architecture

```text
vault_optimizer/
│
├── core/
│   ├── __init__.py
│   ├── scanner.py        # Recursive folder traversal (ignores .git, .obsidian)
│   ├── verifier.py       # Two-stage pixel decompression test
│   ├── converter.py      # Color normalizer & atomic engine (Pillow / FFmpeg)
│   └── rewriter.py       # Markdown link & frontmatter regex rewriter
│
├── optimizer.py          # Interactive terminal interface
├── requirements.txt      # Python dependencies
├── run.bat               # Windows self-bootstrapper
└── README.md             # Documentation