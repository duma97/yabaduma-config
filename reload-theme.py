#!/usr/bin/env python3
"""
Usage:
    reload-theme.py                      # Just reload current colors
    reload-theme.py /path/to/wallpaper   # Set new wallpaper and reload
"""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


class ThemeReloader:
    def __init__(self):
        self.home = Path.home()
        # Dynamically find wal in PATH, fallback to common locations
        self.wal_path = self._find_wal()

    def _find_wal(self) -> Path:
        wal_in_path = shutil.which("wal")
        if wal_in_path:
            return Path(wal_in_path)

        python_versions = ["3.14", "3.13", "3.12", "3.11", "3.10", "3.9"]
        for version in python_versions:
            candidate = self.home / "Library" / "Python" / version / "bin" / "wal"
            if candidate.exists():
                return candidate

        return self.home / "Library" / "Python" / "3.14" / "bin" / "wal"

    def set_wallpaper(self, wallpaper_path: str) -> bool:
        if not Path(wallpaper_path).exists():
            print(f"Error: Wallpaper not found: {wallpaper_path}")
            return False

        print(f"Setting wallpaper: {wallpaper_path}")
        try:
            subprocess.run(
                [str(self.wal_path), "-s", "-t", "-n", "-i", wallpaper_path],
                check=True,
                capture_output=True,
                text=True,
            )
            print("✓ Pywal colors generated")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running pywal: {e}")
            return False
        except FileNotFoundError:
            print(f"Error: pywal not found at {self.wal_path}")
            return False

    def reload_borders(self) -> bool:
        print("Reloading borders with pywal colors...")
        try:
            subprocess.run(
                ["brew", "services", "restart", "borders"],
                check=True,
                capture_output=True,
                text=True,
            )
            print("✓ Borders reloaded")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error reloading borders: {e}")
            return False

    def reload_sketchybar(self) -> bool:
        try:
            result = subprocess.run(
                ["pgrep", "-x", "sketchybar"], capture_output=True, text=True
            )
            if result.returncode != 0:
                print("⊘ Sketchybar not running, skipping reload")
                return False

            print("Reloading sketchybar...")
            subprocess.run(
                ["sketchybar", "--reload"], check=True, capture_output=True, text=True
            )
            print("✓ Sketchybar reloaded")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error reloading sketchybar: {e}")
            return False

    def reload_all(self, wallpaper_path: Optional[str] = None) -> int:
        if wallpaper_path:
            if not self.set_wallpaper(wallpaper_path):
                return 1

        borders_ok = self.reload_borders()
        sketchybar_ok = self.reload_sketchybar()

        print("\n" + "=" * 40)
        if borders_ok or sketchybar_ok:
            print("Theme reloaded successfully!")
            return 0
        else:
            print("Theme reload completed with errors")
            return 1


def main():
    wallpaper = sys.argv[1] if len(sys.argv) > 1 else None

    reloader = ThemeReloader()
    exit_code = reloader.reload_all(wallpaper)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
