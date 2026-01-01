#!/usr/bin/env python3

import json
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


def lighten_color(hex_color, amount):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))

    return f"#{r:02x}{g:02x}{b:02x}"


def lighten_color_by_amount(hex_color, amount):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)

    return f"#{r:02x}{g:02x}{b:02x}"


def update_vscode_settings():
    colors_file = Path.home() / ".cache" / "wal" / "colors.json"
    settings_file = (
        Path.home() / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    )

    if not colors_file.exists():
        print("Pywal colors not found, skipping VSCode update")
        return False

    if not settings_file.exists():
        print("VSCode settings not found, skipping VSCode update")
        return False

    print("Updating VSCode settings...")
    try:
        with open(colors_file) as f:
            wal_colors = json.load(f)

        with open(settings_file) as f:
            vscode_settings = json.load(f)

        bg = wal_colors["special"]["background"]
        fg = wal_colors["special"]["foreground"]
        color1 = wal_colors["colors"]["color1"]
        color2 = wal_colors["colors"]["color2"]
        color3 = wal_colors["colors"]["color3"]
        color4 = wal_colors["colors"]["color4"]
        color6 = wal_colors["colors"]["color6"]
        color8 = wal_colors["colors"]["color8"]

        accent_color = color1
        icon_color = color4
        label_color = color6
        bg_lighter = lighten_color_by_amount(bg, 25)
        selection_bg = lighten_color(bg, 0.25)

        vscode_settings["workbench.colorCustomizations"] = {
            "editor.background": bg_lighter,
            "editor.foreground": label_color,
            "activityBar.background": bg_lighter,
            "activityBar.foreground": icon_color,
            "activityBar.inactiveForeground": color8,
            "activityBar.border": bg_lighter,
            "activityBarBadge.background": accent_color,
            "activityBarBadge.foreground": bg,
            "sideBar.background": bg_lighter,
            "sideBar.foreground": label_color,
            "sideBar.border": bg_lighter,
            "sideBarSectionHeader.background": bg_lighter,
            "sideBarSectionHeader.foreground": label_color,
            "sideBarSectionHeader.border": bg_lighter,
            "statusBar.background": bg_lighter,
            "statusBar.foreground": label_color,
            "statusBar.border": bg_lighter,
            "titleBar.activeBackground": bg_lighter,
            "titleBar.activeForeground": label_color,
            "titleBar.inactiveBackground": bg_lighter,
            "titleBar.inactiveForeground": color8,
            "titleBar.border": bg_lighter,
            "panel.background": bg_lighter,
            "panel.border": bg_lighter,
            "panelTitle.activeBorder": accent_color,
            "panelTitle.activeForeground": label_color,
            "panelTitle.inactiveForeground": color8,
            "editorCursor.foreground": accent_color,
            "editorLineNumber.foreground": color8,
            "editorLineNumber.activeForeground": label_color,
            "editorGutter.background": bg_lighter,
            "editorGutter.addedBackground": color2,
            "editorGutter.modifiedBackground": color3,
            "editorGutter.deletedBackground": accent_color,
            "editor.lineHighlightBackground": bg_lighter,
            "editor.lineHighlightBorder": bg_lighter,
            "editor.selectionBackground": selection_bg,
            "editor.inactiveSelectionBackground": bg_lighter,
            "editorHoverWidget.background": bg_lighter,
            "editorHoverWidget.border": bg_lighter,
            "editorSuggestWidget.background": bg_lighter,
            "editorSuggestWidget.border": bg_lighter,
            "editorSuggestWidget.selectedBackground": selection_bg,
            "scrollbarSlider.background": f"{selection_bg}80",
            "scrollbarSlider.hoverBackground": f"{selection_bg}cc",
            "scrollbarSlider.activeBackground": f"{selection_bg}cc",
            "focusBorder": accent_color,
            "tab.activeBackground": bg_lighter,
            "tab.activeForeground": label_color,
            "tab.inactiveBackground": bg_lighter,
            "tab.inactiveForeground": color8,
            "tab.activeBorder": accent_color,
            "tab.activeBorderTop": accent_color,
            "tab.border": bg_lighter,
            "tab.hoverBackground": bg_lighter,
            "tab.hoverForeground": label_color,
            "editorGroupHeader.tabsBackground": bg_lighter,
            "editorGroupHeader.tabsBorder": bg_lighter,
            "breadcrumb.background": bg_lighter,
            "breadcrumb.foreground": color8,
            "breadcrumb.focusForeground": label_color,
            "breadcrumb.activeSelectionForeground": accent_color,
            "list.activeSelectionBackground": selection_bg,
            "list.activeSelectionForeground": label_color,
            "list.inactiveSelectionBackground": bg_lighter,
            "list.inactiveSelectionForeground": label_color,
            "list.hoverBackground": bg_lighter,
            "list.hoverForeground": label_color,
            "list.focusBackground": selection_bg,
            "list.focusForeground": label_color,
            "list.highlightForeground": accent_color,
            "button.background": accent_color,
            "button.foreground": bg_lighter,
            "button.hoverBackground": color3,
            "button.secondaryBackground": bg_lighter,
            "button.secondaryForeground": label_color,
            "button.secondaryHoverBackground": bg_lighter,
            "input.background": bg_lighter,
            "input.foreground": label_color,
            "input.border": bg_lighter,
            "input.placeholderForeground": color8,
            "inputOption.activeBackground": accent_color,
            "inputOption.activeForeground": bg_lighter,
            "dropdown.background": bg_lighter,
            "dropdown.foreground": label_color,
            "dropdown.border": bg_lighter,
            "notifications.background": bg_lighter,
            "notifications.foreground": label_color,
            "notifications.border": bg_lighter,
            "notificationCenter.border": bg_lighter,
            "notificationCenterHeader.background": bg_lighter,
            "notificationCenterHeader.foreground": label_color,
            "notificationToast.border": bg_lighter,
            "notificationsErrorIcon.foreground": accent_color,
            "notificationsWarningIcon.foreground": color3,
            "notificationsInfoIcon.foreground": icon_color,
            "quickInput.background": bg_lighter,
            "quickInput.foreground": label_color,
            "quickInputList.focusBackground": selection_bg,
            "quickInputList.focusForeground": label_color,
            "quickInputTitle.background": bg_lighter,
            "badge.background": accent_color,
            "badge.foreground": bg_lighter,
            "progressBar.background": accent_color,
            "editorWidget.background": bg_lighter,
            "editorWidget.border": bg_lighter,
            "editorWidget.foreground": label_color,
            "widget.shadow": bg_lighter,
            "settings.headerForeground": label_color,
            "settings.modifiedItemIndicator": accent_color,
            "welcomePage.background": bg_lighter,
            "walkThrough.embeddedEditorBackground": bg_lighter,
        }

        vscode_settings["editor.tokenColorCustomizations"] = {
            "comments": {"foreground": color8, "fontStyle": "italic"},
            "keywords": {"foreground": accent_color, "fontStyle": "bold"},
            "functions": {"foreground": color3, "fontStyle": "bold"},
            "variables": {"foreground": label_color},
            "strings": {"foreground": color2},
            "types": {"foreground": icon_color, "fontStyle": "bold"},
            "numbers": {"foreground": accent_color},
            "textMateRules": [
                {
                    "scope": ["storage.type", "storage.modifier"],
                    "settings": {"foreground": accent_color, "fontStyle": "bold"},
                },
                {
                    "scope": ["entity.name.type", "entity.name.class"],
                    "settings": {"foreground": icon_color, "fontStyle": "bold"},
                },
                {
                    "scope": ["entity.name.function", "support.function"],
                    "settings": {"foreground": color3, "fontStyle": "bold"},
                },
                {
                    "scope": "variable.parameter",
                    "settings": {"foreground": label_color, "fontStyle": "italic"},
                },
                {
                    "scope": "constant.language",
                    "settings": {"foreground": accent_color, "fontStyle": "bold"},
                },
                {
                    "scope": [
                        "punctuation.definition.string",
                        "punctuation.definition.variable",
                        "punctuation.definition.parameters",
                        "punctuation.definition.array",
                    ],
                    "settings": {"foreground": color8},
                },
                {"scope": "punctuation.separator", "settings": {"foreground": label_color}},
                {"scope": "meta.brace", "settings": {"foreground": label_color}},
            ],
        }

        with open(settings_file, "w") as f:
            json.dump(vscode_settings, f, indent=4)

        print("VSCode settings updated")
        return True
    except Exception as e:
        print(f"Error updating VSCode settings: {e}")
        return False


def main():
    wallpaper = sys.argv[1] if len(sys.argv) > 1 else None
    wal_path = find_wal()

    if wallpaper:
        if not set_wallpaper(wal_path, wallpaper):
            sys.exit(1)

    vscode_ok = update_vscode_settings()
    borders_ok = reload_borders()
    sketchybar_ok = reload_sketchybar()

    print("")
    if vscode_ok or borders_ok or sketchybar_ok:
        print("Theme reloaded")
    else:
        print("Theme reload completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
