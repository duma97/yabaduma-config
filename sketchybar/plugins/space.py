#!/usr/bin/env python3

import os
import subprocess


def main():
    name = os.environ.get("NAME", "space")
    selected = os.environ.get("SELECTED", "off")
    subprocess.run(["sketchybar", "--set", name, f"background.drawing={selected}"])


if __name__ == "__main__":
    main()
