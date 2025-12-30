#!/bin/bash

DIRECTION="$1"

case "$DIRECTION" in
    west|east|north|south)
        yabai -m window --swap "$DIRECTION" || \
            (yabai -m window --toggle split && yabai -m window --swap "$DIRECTION")
        ;;
    *)
        echo "Usage: smart-swap.sh <west|east|north|south>" >&2
        exit 1
        ;;
esac
