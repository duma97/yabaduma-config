#!/bin/bash

DIRECTION="$1"

case "$DIRECTION" in
    left)
        yabai -m window --resize left:-50:0 || yabai -m window --resize right:-50:0
        ;;
    right)
        yabai -m window --resize right:50:0 || yabai -m window --resize left:50:0
        ;;
    up)
        yabai -m window --resize top:0:-50 || yabai -m window --resize bottom:0:-50
        ;;
    down)
        yabai -m window --resize bottom:0:50 || yabai -m window --resize top:0:50
        ;;
    *)
        echo "Usage: resize-window.sh <left|right|up|down>" >&2
        exit 1
        ;;
esac
