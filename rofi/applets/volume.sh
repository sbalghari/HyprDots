#!/usr/bin/env bash

# Modified by:  Saifullah Balghari
# Original:     Aditya Shakya (adi1090x)

theme=~/.config/rofi/themes/dmenu.rasi

# Fetch Volume and Microphone Information
get_volume_info() {
    speaker_status=$(amixer get Master | grep -oE '\[on\]|\[off\]' | head -n 1)
    mic_status=$(amixer get Capture | grep -oE '\[on\]|\[off\]' | head -n 1)
    volume=$(amixer get Master | grep -oE '[0-9]+%' | head -n 1)

    if [[ "$speaker_status" == "[on]" ]]; then
        speaker_icon="󰕾"
        speaker_action="Mute Speaker"
    else
        speaker_icon="󰖁"
        speaker_action="Unmute Speaker"
    fi

    if [[ "$mic_status" == "[on]" ]]; then
        mic_icon="󰍬"
        mic_action="Mute Microphone"
    else
        mic_icon="󰍭"
        mic_action="Unmute Microphone"
    fi
}

# Rofi Menu Options
get_menu_options() {
    echo -e "󰕾 Increase Volume(+10)\n󰖁 Decrease Volume(-10)\n${speaker_icon} ${speaker_action}\n${mic_icon} ${mic_action}\n󰘳 Open Settings"
}

# Handle Menu Choices
handle_choice() {
    case "$1" in
        "󰕾 Increase Volume(+10)")
            amixer set Master 10%+
            notify-send "Volume Control" "Volume increased by 10"
            ;;
        "󰖁 Decrease Volume(-10)")
            amixer set Master 10%-
            notify-send "Volume Control" "Volume decreased by 10"
            ;;
        "${speaker_icon} ${speaker_action}")
            amixer set Master toggle
            notify-send "Volume Control" "Speaker ${speaker_action,,}d"
            ;;
        "${mic_icon} ${mic_action}")
            amixer set Capture toggle
            notify-send "Volume Control" "Microphone ${mic_action,,}d"
            ;;
        " Open Settings")
            pavucontrol
            ;;
    esac
}

# Main Function
main() {
    get_volume_info

    choice=$(get_menu_options | rofi -dmenu -i -theme-str 'textbox-prompt-colon {str: " ";}'   -p "Volume ${volume}" -theme "$theme")

    if [[ -n "$choice" ]]; then
        handle_choice "$choice"
    fi
}

main
