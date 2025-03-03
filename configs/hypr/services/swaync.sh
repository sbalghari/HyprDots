#!/bin/bash

get_swaync_pid() {
    pgrep swaync
}

kill_swaync() {
    SWAYNC_PID=$(get_swaync_pid)
    if [ -n "$SWAYNC_PID" ]; then
        kill -9 "$SWAYNC_PID"
        echo "SwayNC killed."
    else
        echo "SwayNC is not running."
    fi
}

start_swaync() {
    SWAYNC_PID=$(get_swaync_pid)
    if [ -z "$SWAYNC_PID" ]; then
        swaync &
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
    kill)
        kill_swaync
        ;;
    start)
        start_swaync
        ;;
    toggle)
        toggle_swaync
        ;;
    reload)
        reload_swaync
        ;;
    *)
        echo "Usage: $0 {kill|start|toggle|reload}"
        exit 1
        ;;
esac

exit 0