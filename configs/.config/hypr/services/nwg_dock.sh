#!/bin/bash

get_nwg_dock_pid() {
    pgrep -f nwg-dock-hyprland
}

kill_nwg_dock() {
    NWG_DOCK_PID=$(get_nwg_dock_pid)
    if [ -n "$NWG_DOCK_PID" ]; then
        kill -9 "$NWG_DOCK_PID"
        sleep 0.2
        echo "nwg-dock-hyprland killed."
    else
        echo "nwg-dock-hyprland is not running."
    fi
}

start_nwg_dock() {
    NWG_DOCK_PID=$(get_nwg_dock_pid)
    if [ -z "$NWG_DOCK_PID" ]; then
        nwg-dock-hyprland -i 34 -d -hd 0&
        sleep 0.2
        echo "nwg-dock-hyprland started."
    else
        echo "nwg-dock-hyprland is already running."
    fi
}

toggle_nwg_dock() {
    NWG_DOCK_PID=$(get_nwg_dock_pid)
    if [ -n "$NWG_DOCK_PID" ]; then
        kill_nwg_dock
    else
        start_nwg_dock
    fi
}

reload_nwg_dock() {
    NWG_DOCK_PID=$(get_nwg_dock_pid)
    if [ -n "$NWG_DOCK_PID" ]; then
        kill_nwg_dock
        start_nwg_dock
        echo "nwg-dock-hyprland reloaded."
    else
        echo "nwg-dock-hyprland is not running. Starting it now..."
        start_nwg_dock
    fi
}

case "$1" in
    -k | --kill)
        kill_nwg_dock
        ;;
    -s | --start)
        start_nwg_dock
        ;;
    -t | --toggle)
        toggle_nwg_dock
        ;;
    -r | --reload)
        reload_nwg_dock
        ;;
    -h | --help)
        echo "Usage: $0 [option]"
        echo "Options:"
        echo "  -k, --kill      Kill nw-dock-hyprland"
        echo "  -s, --start     Start nwg-dock-hyprland"
        echo "  -t, --toggle    Toggle nwg-dock-hyprland"
        echo "  -r, --reload    Reload nwg-dock-hyprland"
        exit 0
        ;;
    *)
        echo "Invalid option. Use -h/--help for more information."
        exit 1
        ;;
esac

exit 0