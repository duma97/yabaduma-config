#!/bin/bash
# smart-swap.sh - Smart window swap with split toggle fallback
#
# Usage: smart-swap.sh <direction>
# Directions: west, east, north, south
#
# Attempts to swap windows in the given direction. If that fails,
# toggles the split orientation and tries again.

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
