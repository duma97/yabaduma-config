#!/usr/bin/env python3

import shutil
import subprocess
import sys
from pathlib import Path


def find_wal():
    wal_in_path = shutil.which("wal")
    if wal_in_path:
        return Path(wal_in_path)

    home = Path.home()
    for version in ["3.14", "3.13", "3.12", "3.11", "3.10", "3.9"]:
        candidate = home / "Library" / "Python" / version / "bin" / "wal"
        if candidate.exists():
            return candidate

    return home / "Library" / "Python" / "3.14" / "bin" / "wal"


def set_wallpaper(wal_path, wallpaper_path):
    if not Path(wallpaper_path).exists():
        print(f"Error: Wallpaper not found: {wallpaper_path}")
        return False

    print(f"Setting wallpaper: {wallpaper_path}")
    try:
        subprocess.run(
            [str(wal_path), "-s", "-t", "-n", "-i", wallpaper_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Pywal colors generated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running pywal: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: pywal not found at {wal_path}")
        return False


def reload_borders():
    print("Reloading borders...")
    try:
        subprocess.run(
            ["brew", "services", "restart", "borders"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Borders reloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reloading borders: {e}")
        return False


def reload_sketchybar():
    result = subprocess.run(
        ["pgrep", "-x", "sketchybar"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Sketchybar not running, skipping")
        return False

    print("Reloading sketchybar...")
    try:
        subprocess.run(
            ["sketchybar", "--reload"], check=True, capture_output=True, text=True
        )
        print("Sketchybar reloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reloading sketchybar: {e}")
        return False


def main():
    wallpaper = sys.argv[1] if len(sys.argv) > 1 else None
    wal_path = find_wal()

    if wallpaper:
        if not set_wallpaper(wal_path, wallpaper):
            sys.exit(1)

    borders_ok = reload_borders()
    sketchybar_ok = reload_sketchybar()

    print("")
    if borders_ok or sketchybar_ok:
        print("Theme reloaded")
    else:
        print("Theme reload completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
