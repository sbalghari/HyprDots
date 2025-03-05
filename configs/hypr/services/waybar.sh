#!/bin/bash

get_waybar_pid() {
    pgrep waybar
}

kill_waybar() {
    WAYBAR_PID=$(get_waybar_pid)
    if [ -n "$WAYBAR_PID" ]; then
        kill -9 "$WAYBAR_PID"
        echo "Waybar killed."
    else
        echo "Waybar is not running."
    fi
}

start_waybar() {
    WAYBAR_PID=$(get_waybar_pid)
    if [ -z "$WAYBAR_PID" ]; then
        waybar &
        echo "Waybar started."
    else
        echo "Waybar is already running."
    fi
}

toggle_waybar() {
    WAYBAR_PID=$(get_waybar_pid)
    if [ -n "$WAYBAR_PID" ]; then
        kill_waybar
    else
        start_waybar
    fi
}

reload_waybar() {
    WAYBAR_PID=$(get_waybar_pid)
    if [ -n "$WAYBAR_PID" ]; then
        kill_waybar
        start_waybar
        echo "Waybar reloaded."
    else
        echo "Waybar is not running. Starting it now..."
        start_waybar
    fi
}

case "$1" in
    -k | --kill)
        kill_waybar
        ;;
    -s | --start)
        start_waybar
        ;;
    -t | --toggle)
        toggle_waybar
        ;;
    -r | --reload)
        reload_waybar
        ;;
    -h | --help)
        echo "Usage: $0 [OPTION]"
        echo "Options:"
        echo "  -k, --kill      Kill Waybar"
        echo "  -s, --start     Start Waybar"
        echo "  -t, --toggle    Toggle Waybar"
        echo "  -r, --reload    Reload Waybar"
        echo "  -h, --help      Display this help message"
        exit 0
        ;;
    *)
        echo "Invalid option. Use -h/--help for more information."
        exit 1
        ;;
esac

exit 0