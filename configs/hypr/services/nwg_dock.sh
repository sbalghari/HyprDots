#!/bin/bash

get_nwg_dock_pid() {
    pgrep nwg-dock-hyprland
}

kill_nwg_dock() {
    NWG_DOCK_PID=$(get_nwg_dock_pid)
    if [ -n "$NWG_DOCK_PID" ]; then
        kill -9 "$NWG_DOCK_PID"
        echo "nwg-dock-hyprland killed."
    else
        echo "nwg-dock-hyprland is not running."
    fi
}

start_nwg_dock() {
    NWG_DOCK_PID=$(get_nwg_dock_pid)
    if [ -z "$NWG_DOCK_PID" ]; then
        nwg-dock-hyprland &
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
    kill)
        kill_nwg_dock
        ;;
    start)
        start_nwg_dock
        ;;
    toggle)
        toggle_nwg_dock
        ;;
    reload)
        reload_nwg_dock
        ;;
    *)
        echo "Usage: $0 {kill|start|toggle|reload}"
        exit 1
        ;;
esac

exit 0