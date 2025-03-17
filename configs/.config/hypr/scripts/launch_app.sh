#!/bin/bash

# Ensure a program name is provided
if [ -z "$1" ]; then
  notify-send "Error" "No program specified. Please provide a program to run."
  exit 1
fi

sleep 0.2
program="$1"

# Check if the program exists in the system
if ! command -v "$program" >/dev/null 2>&1; then
  notify-send "Program not found" "Make sure you have installed $program"
  exit 1
fi

# Execute the program
exec "$program"

exit 0