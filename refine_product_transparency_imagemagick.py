import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("product/tshirt 01 to 18")
IMAGE_GLOB = "TSH-*/*.png"


def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def identify_image(path: Path):
    data = run(["identify", "-format", "%w %h %[channels]", str(path)])
    w, h, channels = data.split(" ", 2)
    return int(w), int(h), channels


def alpha_mean(path: Path):
    try:
        return float(run(["convert", str(path), "-alpha", "extract", "-format", "%[fx:mean]", "info:"]))
    except Exception:
        return 1.0


def resize_percent(width: int, height: int) -> int:
    longest = max(width, height)
    if longest < 900:
        return 150
    if longest < 1300:
        return 125
    return 100


def process_image(path: Path):
    width, height, channels = identify_image(path)
    alpha = alpha_mean(path)
    resize_pct = resize_percent(width, height)
    old_size = path.stat().st_size

    fd, tmp_name = tempfile.mkstemp(suffix=".png", dir=str(path.parent))
    os.close(fd)
    tmp_path = Path(tmp_name)

    cmd = [
        "convert",
        str(path),
        "-background",
        "none",
        "-alpha",
        "on",
    ]

    # If a file is almost fully opaque, try to force transparency from the outer border first.
    if "a" not in channels.lower() or alpha >= 0.995:
        w1 = width - 1
        h1 = height - 1
        wm = width // 2
        hm = height // 2
        cmd += [
            "-fuzz",
            "14%",
            "-fill",
            "none",
            "-draw",
            f"color 0,0 floodfill color {w1},0 floodfill color 0,{h1} floodfill color {w1},{h1} floodfill color {wm},0 floodfill color {wm},{h1} floodfill color 0,{hm} floodfill color {w1},{hm} floodfill",
        ]

    cmd += [
        "-channel",
        "A",
        "-level",
        "3%,94%",
        "+channel",
    ]

    if resize_pct != 100:
        cmd += ["-filter", "LanczosSharp", "-resize", f"{resize_pct}%"]

    cmd += [
        "-unsharp",
        "0x0.8+0.8+0.03",
        "-strip",
        "-define",
        "png:compression-level=9",
        "-define",
        "png:compression-strategy=1",
        "png32:" + str(tmp_path),
    ]

    subprocess.check_call(cmd)
    tmp_path.replace(path)
    new_size = path.stat().st_size

    return {
        "path": str(path),
        "width": width,
        "height": height,
        "channels": channels,
        "alpha_mean": alpha,
        "resize_pct": resize_pct,
        "old_size": old_size,
        "new_size": new_size,
    }


def main():
    files = sorted(ROOT.glob(IMAGE_GLOB))
    total_old = 0
    total_new = 0
    resized = 0
    processed = []

    print(f"Found {len(files)} product PNG files to refine...")

    for path in files:
        result = process_image(path)
        total_old += result["old_size"]
        total_new += result["new_size"]
        if result["resize_pct"] != 100:
            resized += 1
        processed.append(result)
        print(
            f"✅ {path.name:<16} | {result['width']}x{result['height']} | alpha={result['alpha_mean']:.3f} | "
            f"resize={result['resize_pct']}% | {result['old_size'] / 1024:.1f}KB -> {result['new_size'] / 1024:.1f}KB"
        )

    print("\nDone.")
    print(f"Processed: {len(processed)} files")
    print(f"Upscaled:  {resized} files")
    print(f"Old size:  {total_old / (1024 * 1024):.2f} MB")
    print(f"New size:  {total_new / (1024 * 1024):.2f} MB")
    if total_old:
        pct = ((total_new - total_old) / total_old) * 100
        direction = "increase" if pct >= 0 else "decrease"
        print(f"Net {direction}: {abs(pct):.1f}%")


if __name__ == "__main__":
    main()
