#!/bin/bash

# Settings path
CURRENT_APP_LAUNCHER="$HOME/.user_settings/app_launcher.sh"

# Default app launcher
APP_LAUNCHER="rofi"

# loads the current app launcher if exists
if [ -f "$CURRENT_APP_LAUNCHER" ]; then
    source "$CURRENT_APP_LAUNCHER"
fi

# Function to launch rofi
launch_rofi() {
    rofi -show drun  -theme "$HOME/.config/rofi/configs/launcher.rasi"
}

# Function to launch nwg_drawer
launch_nwg_drawer() {
    nwg-drawer -fm "nautilus" \
        -term "kitty" \
        -is 72 \
        -c 4 \
        -mr 540 \
        -ml 540 \
        -mt 400 \
        -spacing 16\
        -nofs \
        -ovl \
        -nocats \
        -pbsize 16
}

case "$APP_LAUNCHER" in
    rofi)
        launch_rofi
        ;;
    nwg_drawer)
        launch_nwg_drawer
        ;;
    *)
        echo "Error!"
        exit 1
        ;;
esac

exit 0