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


def update_zed_theme():
    colors_file = Path.home() / ".cache" / "wal" / "colors.json"
    zed_themes_dir = Path.home() / ".config" / "zed" / "themes"
    theme_file = zed_themes_dir / "pywal.json"
    settings_file = Path.home() / ".config" / "zed" / "settings.json"

    if not colors_file.exists():
        print("Pywal colors not found, skipping Zed update")
        return False

    if not zed_themes_dir.exists():
        print("Zed themes directory not found, skipping Zed update")
        return False

    print("Updating Zed theme...")
    try:
        with open(colors_file) as f:
            wal_colors = json.load(f)

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

        zed_theme = {
            "$schema": "https://zed.dev/schema/themes/v0.1.0.json",
            "name": "Pywal",
            "author": "Auto-generated from pywal",
            "themes": [
                {
                    "name": "Pywal",
                    "appearance": "dark",
                    "style": {
                        "border": bg_lighter,
                        "border.variant": bg_lighter,
                        "border.focused": accent_color,
                        "border.selected": accent_color,
                        "border.transparent": "#00000000",
                        "border.disabled": bg_lighter,
                        "elevated_surface.background": bg_lighter,
                        "surface.background": bg_lighter,
                        "background": bg_lighter,
                        "element.background": bg_lighter,
                        "element.hover": selection_bg,
                        "element.active": selection_bg,
                        "element.selected": selection_bg,
                        "element.disabled": bg_lighter,
                        "drop_target.background": f"{selection_bg}cc",
                        "ghost_element.background": "#00000000",
                        "ghost_element.hover": selection_bg,
                        "ghost_element.active": selection_bg,
                        "ghost_element.selected": selection_bg,
                        "ghost_element.disabled": bg_lighter,
                        "text": label_color,
                        "text.muted": color8,
                        "text.placeholder": color8,
                        "text.disabled": color8,
                        "text.accent": accent_color,
                        "icon": icon_color,
                        "icon.muted": color8,
                        "icon.disabled": color8,
                        "icon.placeholder": color8,
                        "icon.accent": accent_color,
                        "status_bar.background": bg_lighter,
                        "title_bar.background": bg_lighter,
                        "toolbar.background": bg_lighter,
                        "tab_bar.background": bg_lighter,
                        "tab.inactive_background": bg_lighter,
                        "tab.active_background": bg_lighter,
                        "search.match_background": selection_bg,
                        "panel.background": bg_lighter,
                        "panel.focused_border": accent_color,
                        "pane.focused_border": accent_color,
                        "scrollbar.thumb.background": f"{selection_bg}80",
                        "scrollbar.thumb.hover_background": f"{selection_bg}cc",
                        "scrollbar.thumb.border": "#00000000",
                        "scrollbar.track.background": "#00000000",
                        "scrollbar.track.border": "#00000000",
                        "editor.foreground": label_color,
                        "editor.background": bg_lighter,
                        "editor.gutter.background": bg_lighter,
                        "editor.subheader.background": bg_lighter,
                        "editor.active_line.background": bg_lighter,
                        "editor.highlighted_line.background": bg_lighter,
                        "editor.line_number": color8,
                        "editor.active_line_number": label_color,
                        "editor.invisible": color8,
                        "editor.wrap_guide": bg_lighter,
                        "editor.active_wrap_guide": bg_lighter,
                        "editor.document_highlight.read_background": f"{selection_bg}80",
                        "editor.document_highlight.write_background": f"{selection_bg}80",
                        "terminal.background": bg_lighter,
                        "terminal.foreground": label_color,
                        "terminal.ansi.black": bg,
                        "terminal.ansi.bright_black": color8,
                        "terminal.ansi.dim_black": bg,
                        "terminal.ansi.red": accent_color,
                        "terminal.ansi.bright_red": accent_color,
                        "terminal.ansi.dim_red": accent_color,
                        "terminal.ansi.green": color2,
                        "terminal.ansi.bright_green": color2,
                        "terminal.ansi.dim_green": color2,
                        "terminal.ansi.yellow": color3,
                        "terminal.ansi.bright_yellow": color3,
                        "terminal.ansi.dim_yellow": color3,
                        "terminal.ansi.blue": icon_color,
                        "terminal.ansi.bright_blue": icon_color,
                        "terminal.ansi.dim_blue": icon_color,
                        "terminal.ansi.magenta": color3,
                        "terminal.ansi.bright_magenta": color3,
                        "terminal.ansi.dim_magenta": color3,
                        "terminal.ansi.cyan": label_color,
                        "terminal.ansi.bright_cyan": label_color,
                        "terminal.ansi.dim_cyan": label_color,
                        "terminal.ansi.white": label_color,
                        "terminal.ansi.bright_white": label_color,
                        "terminal.ansi.dim_white": label_color,
                        "link_text.hover": accent_color,
                        "conflict": accent_color,
                        "conflict.background": bg_lighter,
                        "conflict.border": accent_color,
                        "created": color2,
                        "created.background": bg_lighter,
                        "created.border": color2,
                        "deleted": accent_color,
                        "deleted.background": bg_lighter,
                        "deleted.border": accent_color,
                        "error": accent_color,
                        "error.background": bg_lighter,
                        "error.border": accent_color,
                        "hidden": color8,
                        "hidden.background": bg_lighter,
                        "hidden.border": color8,
                        "hint": icon_color,
                        "hint.background": bg_lighter,
                        "hint.border": icon_color,
                        "ignored": color8,
                        "ignored.background": bg_lighter,
                        "ignored.border": color8,
                        "info": icon_color,
                        "info.background": bg_lighter,
                        "info.border": icon_color,
                        "modified": color3,
                        "modified.background": bg_lighter,
                        "modified.border": color3,
                        "predictive": color8,
                        "predictive.background": bg_lighter,
                        "predictive.border": color8,
                        "renamed": color2,
                        "renamed.background": bg_lighter,
                        "renamed.border": color2,
                        "success": color2,
                        "success.background": bg_lighter,
                        "success.border": color2,
                        "unreachable": color8,
                        "unreachable.background": bg_lighter,
                        "unreachable.border": color8,
                        "warning": color3,
                        "warning.background": bg_lighter,
                        "warning.border": color3,
                        "players": [],
                        "syntax": {
                            "attribute": {"color": label_color},
                            "boolean": {"color": accent_color, "font_weight": 700},
                            "comment": {"color": color8, "font_style": "italic"},
                            "comment.doc": {"color": color8, "font_style": "italic"},
                            "constant": {"color": accent_color, "font_weight": 700},
                            "constructor": {"color": color3, "font_weight": 700},
                            "embedded": {"color": label_color},
                            "emphasis": {"font_style": "italic"},
                            "emphasis.strong": {"font_weight": 700},
                            "enum": {"color": icon_color, "font_weight": 700},
                            "function": {"color": color3, "font_weight": 700},
                            "hint": {"color": color8, "font_weight": 700},
                            "keyword": {"color": accent_color, "font_weight": 700},
                            "label": {"color": label_color},
                            "link_text": {"color": accent_color, "font_style": "italic"},
                            "link_uri": {"color": accent_color},
                            "number": {"color": accent_color},
                            "operator": {"color": label_color},
                            "predictive": {"color": color8, "font_style": "italic"},
                            "preproc": {"color": label_color},
                            "primary": {"color": label_color},
                            "property": {"color": label_color},
                            "punctuation": {"color": color8},
                            "punctuation.bracket": {"color": label_color},
                            "punctuation.delimiter": {"color": label_color},
                            "punctuation.list_marker": {"color": label_color},
                            "punctuation.special": {"color": color8},
                            "string": {"color": color2},
                            "string.escape": {"color": color8},
                            "string.regex": {"color": color2},
                            "string.special": {"color": color2},
                            "string.special.symbol": {"color": color2},
                            "tag": {"color": icon_color},
                            "text.literal": {"color": color2},
                            "title": {"color": accent_color, "font_weight": 700},
                            "type": {"color": icon_color, "font_weight": 700},
                            "variable": {"color": label_color},
                            "variable.special": {"color": label_color, "font_style": "italic"},
                            "variant": {"color": icon_color},
                        },
                    },
                }
            ],
        }

        with open(theme_file, "w") as f:
            json.dump(zed_theme, f, indent=2)

        if settings_file.exists():
            with open(settings_file) as f:
                content = f.read()

            import re
            updated_content = re.sub(
                r'"theme":\s*\{[^}]*"dark":\s*"[^"]*"',
                '"theme": {\n    "mode": "system",\n    "light": "Ayu Light",\n    "dark": "Pywal"',
                content,
            )

            with open(settings_file, "w") as f:
                f.write(updated_content)

        print("Zed theme updated")
        return True
    except Exception as e:
        print(f"Error updating Zed theme: {e}")
        return False


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

    zed_ok = update_zed_theme()
    vscode_ok = update_vscode_settings()
    borders_ok = reload_borders()
    sketchybar_ok = reload_sketchybar()

    print("")
    if zed_ok or vscode_ok or borders_ok or sketchybar_ok:
        print("Theme reloaded")
    else:
        print("Theme reload completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
