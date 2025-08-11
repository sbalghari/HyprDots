#!/bin/bash

get_swaync_pid() {
    pgrep swaync
}

kill_swaync() {
    SWAYNC_PID=$(get_swaync_pid)
    if [ -n "$SWAYNC_PID" ]; then
        kill -9 "$SWAYNC_PID"
        sleep 0.2
        echo "SwayNC killed."
    else
        echo "SwayNC is not running."
    fi
}

start_swaync() {
    SWAYNC_PID=$(get_swaync_pid)
    if [ -z "$SWAYNC_PID" ]; then
        swaync &
        sleep 0.2
        echo "SwayNC started."
    else
        echo "SwayNC is already running."
    fi
}

toggle_swaync() {
    SWAYNC_PID=$(get_swaync_pid)
    if [ -n "$SWAYNC_PID" ]; then
        kill_swaync
    else
        start_swaync
    fi
}

reload_swaync() {
    SWAYNC_PID=$(get_swaync_pid)
    if [ -n "$SWAYNC_PID" ]; then
        kill_swaync
        start_swaync
        echo "SwayNC reloaded."
    else
        echo "SwayNC is not running. Starting it now..."
        start_swaync
    fi
}

case "$1" in
    -k | --kill)
        kill_swaync
        ;;
    -s | --start)
        start_swaync
        ;;
    -t | --toggle)
        toggle_swaync
        ;;
    -r | --reload)
        reload_swaync
        ;;
    -h | --help)
        echo "Usage: swaync.sh [OPTION]"
        echo "Options:"
        echo "  -k, --kill      Kill SwayNC"
        echo "  -s, --start     Start SwayNC"
        echo "  -t, --toggle    Toggle SwayNC"
        echo "  -r, --reload    Reload SwayNC"
        echo "  -h, --help      Display this help message"
        exit 0
        ;;
    *)
        echo "Invalid option. Use -h/--help for more information."
        exit 1
        ;;
esac

exit 0