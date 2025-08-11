#!/bin/bash

# Define thresholds for color indicators
threshhold_none=0
threshhold_green=1
threshhold_yellow=25
threshhold_red=50

# Detect platform
if [[ -f /etc/arch-release ]]; then
    # AUR helper detection
    aur_helper=$(command -v yay || command -v paru || echo "")
    if [[ -z "$aur_helper" ]]; then
        echo " ERROR - No AUR helper found (yay or paru)."
        exit 1
    fi
else
    echo '{"text": "Unsupported platform"}'
    exit 1
fi

# Check dependencies
if ! command -v checkupdates-with-aur &> /dev/null; then
    echo '{"text": "Missing checkupdates-with-aur"}'
    exit 1
fi

if ! command -v "$aur_helper" &> /dev/null; then
    echo '{"text": "Missing AUR helper: '"$aur_helper"'"}'
    exit 1
fi

# Calculate updates
aur_updates=$(checkupdates-with-aur 2>/dev/null | wc -l)
flatpak_updates=$(flatpak remote-ls --updates 2>/dev/null | wc -l)
updates=$((aur_updates + flatpak_updates))

# Determine CSS class
css_class="none"
if [ "$updates" -ge "$threshhold_green" ]; then
    css_class="green"
fi
if [ "$updates" -ge "$threshhold_yellow" ]; then
    css_class="yellow"
fi
if [ "$updates" -ge "$threshhold_red" ]; then
    css_class="red"
fi

# Output in JSON format
if [ "$updates" -le "$threshhold_none" ]; then
    printf '{"text": "", "class": "none"}'
else
    printf '{"text": " %s", "alt": "%s", "tooltip": "System updates: %s", "class": "%s"}' "$updates" "$updates" "$updates" "$css_class"
fi

exit 0