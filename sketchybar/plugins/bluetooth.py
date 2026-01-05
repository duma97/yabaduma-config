#!/usr/bin/env python3

import os
import shutil
import subprocess

ICON_CONNECTED = "󰂱"
ICON_ON = "󰂯"
ICON_OFF = "󰂲"


def get_bluetooth_power() -> bool:
    result = subprocess.run(
        ["blueutil", "-p"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() == "1"


def get_connected_count() -> int:
    result = subprocess.run(
        ["blueutil", "--connected"],
        capture_output=True,
        text=True,
    )
    if not result.stdout.strip():
        return 0
    return result.stdout.count("address")


def main():
    name = os.environ.get("NAME", "bluetooth")

    if not shutil.which("blueutil"):
        subprocess.run(["sketchybar", "--set", name, f"icon={ICON_OFF}", "label=N/A"])
        return

    if not get_bluetooth_power():
        subprocess.run(["sketchybar", "--set", name, f"icon={ICON_OFF}", "label="])
        return

    count = get_connected_count()
    if count > 0:
        subprocess.run(
            ["sketchybar", "--set", name, f"icon={ICON_CONNECTED}", f"label={count}"]
        )
    else:
        subprocess.run(["sketchybar", "--set", name, f"icon={ICON_ON}", "label="])


if __name__ == "__main__":
    main()
