#!/bin/bash

# Log file
SBHD_DIR="$HOME/sbhd/"
LOG_FILE="$SBHD_DIR/installer.log"

log() {
    local level=$1
    local message=$2
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # Log to stdout
    echo "[${timestamp}] [${level}] ${message}"

    # Log to LOG_FILE
    if [ -n "${LOG_FILE}" ]; then
        echo "[${timestamp}] [${level}] ${message}" >> "${LOG_FILE}"
    fi
}