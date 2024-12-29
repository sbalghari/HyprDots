#!/bin/bash

# Paths
WAL_CSS="$HOME/.cache/wal/colors.css"
COLORS_CONF="$HOME/.config/hypr/configs/colors.conf"

# parsing colors from wal
fg_hex=$(grep -oP '(?<=--color11: )#[0-9a-fA-F]+' "$WAL_CSS")
bg_hex=$(grep -oP '(?<=--color0: )#[0-9a-fA-F]+' "$WAL_CSS")

# ARGB converting function
hex_to_argb() {
    local hex="$1"
    local alpha="b3"
    local rr="${hex:1:2}"
    local gg="${hex:3:2}"
    local bb="${hex:5:2}"
    echo "0x${alpha}${rr}${gg}${bb}"
}

# Convert hex colors to ARGB
fg=$(hex_to_argb "$fg_hex")
bg=$(hex_to_argb "$bg_hex")
echo "$fg"
echo "$bg"

# Update colors.conf
if [[ -n $fg && -n $bg ]]; then
    : > $COLORS_CONF
    echo "\$fg = $fg" >> $COLORS_CONF
    echo "\$bg = $bg" >> $COLORS_CONF
else
    echo "Error: Could not extract or convert colors."
fi
