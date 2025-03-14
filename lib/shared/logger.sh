#!/bin/bash

# Log file
LOG_FILE="${HOME}/dotfiles_install.log"

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