#!/usr/bin/env bash

# Modified by:  Saifullah Balghari
# Original:     Aditya Shakya (adi1090x)

theme=~/.config/rofi/themes/dmenu.rasi

# Battery Info using upower
battery="`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep 'model:' | awk '{print $2}'`"
status="`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep 'state:' | awk '{print $2}'`"
percentage="`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep 'percentage:' | awk '{print $2}' | tr -d '%'`"
time0="`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep 'time to full:' | awk -F':' '{print $2":"$3}' | xargs`"
time1="`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep 'time to empty:' | awk -F':' '{print $2":"$3}' | xargs`"

# Power Profiles Info
current_profile=$(powerprofilesctl get)

title="Power-Profiles"
mesg=""

if [[ $status == "fully-charged" ]]; then
    mesg="${status}"
elif [[ $status == "discharging" ]]; then
    mesg="${status}, ${time1} left"
elif [[ $status == "charging" ]]; then
    mesg="${status}, ${time0} left"
fi

list_col='1'
list_row='3'
win_width='400px'

option_1="  Percentage: ${percentage}%"
option_2="  Toggle Power Saver (${current_profile^})"
option_3="󱊦  Enable Performance Mode"

# Rofi CMD
rofi_cmd() {
    rofi -theme-str "window {width: $win_width;}" \
        -theme-str 'textbox-prompt-colon {str: "󱊣";}' \
        -theme-str "listview {columns: $list_col; lines: $list_row;}" \
        -dmenu \
        -p "$title" \
        -mesg "$mesg" \
        ${active} ${urgent} \
        -theme ${theme}
}

# Pass variables to rofi dmenu
run_rofi() {
    echo -e "$option_1\n$option_2\n$option_3" | rofi_cmd
}

# Execute Command
run_cmd() {
    polkit_cmd="pkexec env PATH=$PATH DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY"
    if [[ "$1" == '--opt1' ]]; then
        notify-send -u low "$ICON_CHRG Status : $status"
    elif [[ "$1" == '--opt2' ]]; then
        if [[ $current_profile == "power-saver" ]]; then
            powerprofilesctl set balanced
            notify-send -u low "Power Profile" "Switched to Balanced"
        else
            powerprofilesctl set power-saver
            light -S 50
            notify-send -u low "Power Profile" "Switched to Power Saver"
        fi
    elif [[ "$1" == '--opt3' ]]; then
        powerprofilesctl set performance
        light -S 100
        notify-send -u critical "Power Profile" "Performance Mode Enabled"
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
esac
