#!/usr/bin/env bash

# Modified by:  Saifullah Balghari
# Original:     Aditya Shakya (adi1090x)

theme=~/.config/rofi/themes/dmenu.rasi

status="$(playerctl status 2>/dev/null)"
if [[ -z "$status" ]]; then
    title='No Player Found'
    mesg="No media player is currently active."
else
    title="$(playerctl metadata artist)"
    mesg="$(playerctl metadata title)"
fi

list_col='1'
list_row='6'

if [[ ${status} == "Playing" ]]; then
    option_1="  Pause"
else
    option_1="  Play"
fi
option_2="  Stop"
option_3="󰙣  Previous"
option_4="󰙡  Next"
option_5="  Loop"
option_6="  Shuffle"

# Toggle Actions
active=''
urgent=''

# Rofi CMD
rofi_cmd() {
    rofi -theme-str "listview {columns: $list_col; lines: $list_row;}" \
        -theme-str 'textbox-prompt-colon {str: " ";}' \
        -dmenu \
        -p "$title" \
        -mesg "$mesg" \
        ${active} ${urgent} \
        -markup-rows \
        -theme ${theme}
}

# Pass variables to rofi dmenu
run_rofi() {
    echo -e "$option_1\n$option_2\n$option_3\n$option_4\n$option_5\n$option_6" | rofi_cmd
}

# Execute Command
run_cmd() {
    if [[ "$1" == '--opt1' ]]; then
        playerctl play-pause && notify-send -u low -t 1000 " $(playerctl metadata title)"
    elif [[ "$1" == '--opt2' ]]; then
        playerctl stop
    elif [[ "$1" == '--opt3' ]]; then
        playerctl previous && notify-send -u low -t 1000 " $(playerctl metadata title)"
    elif [[ "$1" == '--opt4' ]]; then
        playerctl next && notify-send -u low -t 1000 " $(playerctl metadata title)"
    elif [[ "$1" == '--opt5' ]]; then
        current_loop=$(playerctl loop)
        if [[ "$current_loop" == "Track" ]]; then
            playerctl loop none
            notify-send -u low -t 1000 "Loop is turned off"
        elif [[ "$current_loop" == "None" ]]; then
            playerctl loop track
            notify-send -u low -t 1000 "Loop is turned on"
        else
            notify-send -u critical -t 2000 "Error: Unexpected loop status: $current_loop"
        fi
    elif [[ "$1" == '--opt6' ]]; then
        current_shuffle=$(playerctl shuffle)
        if [[ "$current_shuffle" == "On" ]]; then
            playerctl shuffle off
            notify-send -u low -t 1000 "Shuffle is turned off"
        elif [[ "$current_shuffle" == "Off" ]]; then
            playerctl shuffle on
            notify-send -u low -t 1000 "Shuffle is turned on"
        else
            notify-send -u critical -t 2000 "Error: Unexpected shuffle status: $current_shuffle"
        fi
    fi
}

# Actions
chosen="$(run_rofi)"
case ${chosen} in
    $option_1)
        run_cmd --opt1
        ;;
    $option_2)
        run_cmd --opt2
        ;;
    $option_3)
        run_cmd --opt3
        ;;
    $option_4)
        run_cmd --opt4
        ;;
    $option_5)
        run_cmd --opt5
        ;;
    $option_6)
        run_cmd --opt6
        ;;
esac
