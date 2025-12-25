#!/bin/bash

# Check if pywal colors exist, otherwise use defaults
if [ -f ~/.cache/wal/colors.sh ]; then
    # Source pywal colors
    source ~/.cache/wal/colors.sh

    # Export colors in sketchybar format (0xAARRGGBB)
    # Convert #RRGGBB to 0xffRRGGBB
    export BAR_COLOR="0xff${background:1}"
    export ITEM_BG_COLOR="0xff${color0:1}"
    export ACCENT_COLOR="0xff${color1:1}"
    export ICON_COLOR="0xff${foreground:1}"
    export LABEL_COLOR="0xff${foreground:1}"
    export POPUP_BACKGROUND_COLOR="0xff${color0:1}"
    export POPUP_BORDER_COLOR="0xff${color8:1}"
    export SHADOW_COLOR="0x80000000"
else
    # Fallback colors (original colors)
    export BAR_COLOR="0x00000000"
    export ITEM_BG_COLOR="0xf01e3a5f"
    export ACCENT_COLOR="0xff5f87af"
    export ICON_COLOR="0xffDFE5F3"
    export LABEL_COLOR="0xffDFE5F3"
    export POPUP_BACKGROUND_COLOR="0xff1e3a5f"
    export POPUP_BORDER_COLOR="0xff5f87af"
    export SHADOW_COLOR="0x80000000"
fi
