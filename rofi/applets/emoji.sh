#!/usr/bin/env bash

# Theme Configuration (Ensure the path is correct)
theme="$HOME/.config/rofi/themes/emoji.rasi"

# Rofi Command to Display Emojis with a Searchable Message (mesg)
rofi_cmd() {
    rofi -modi emoji -show emoji -emoji-mode copy \
         -theme "$theme" \
         -theme-str 'textbox-prompt-colon {str: "󰞅 ";}' \
         -emoji-format '{emoji} <span weight="bold">{name}</span> [<span size="small">({group})</span>]' 
}

# Execute Rofi Command to pick emoji
chosen="$(rofi_cmd)"

# If a valid emoji is chosen, copy it to clipboard
if [[ -n "$chosen" ]]; then
    wl-copy <<< "$chosen"
    notify-send "Emoji copied to clipboard!" "$chosen"
else
    exit 1
fi
