#!/bin/bash

# Theme
theme="$HOME/.config/rofi/themes/dmenu.rasi"
toggle_icon=""

if nmcli radio wifi | grep -q "enabled"; then
    toggle_icon=""
elif nmcli radio wifi | grep -q "disabled"; then
    toggle_icon=""
fi

# Define options
OPTIONS="${toggle_icon}  Toggle Wi-fi\n直 Connect to Network\n  View IP Address\n  Exit"

# Rofi menu
CHOICE=$(echo -e "$OPTIONS" | rofi -dmenu -l 4 -i -theme-str 'textbox-prompt-colon {str: " ";}' -p "Network Settings" -theme "$theme")

toggle_wifi() {
    if nmcli radio wifi | grep -q "enabled"; then
        disable_wifi
    elif nmcli radio wifi | grep -q "disabled"; then
        enable_wifi
    fi

}

# Functions
enable_wifi() {
    nmcli radio wifi on
    notify-send "Network Menu" "Wi-Fi Enabled"
}

disable_wifi() {
    nmcli radio wifi off
    notify-send "Network Menu" "Wi-Fi Disabled"
}

scan_and_connect() {
    # Check if Wi-Fi is enabled
    if ! nmcli radio wifi | grep -q "enabled"; then
        notify-send "Network Menu" "Wi-Fi is disabled. Please enable Wi-Fi first."
        return
    fi

    # Scan for networks
    nmcli dev wifi rescan
    sleep 0.4

    # List available networks with SSIDs only
    SSID=$(nmcli -t -f SSID dev wifi | awk NF | sort -u | rofi -dmenu -i -theme-str 'textbox-prompt-colon {str: " ";}'  -p "Available Networks" -theme "$theme")

    if [ -n "$SSID" ]; then
        # Check if already connected
        if nmcli -t -f ACTIVE,SSID dev wifi | grep -q "yes:$SSID"; then
            notify-send "Network Menu" "Already connected to $SSID"
        else
            # Use Zenity to prompt for password
            PASSWORD=$(zenity --entry --title="Network Menu" --text="Enter password for $SSID:" --hide-text)

            if [ -n "$PASSWORD" ]; then
                # Attempt connection
                nmcli dev wifi connect "$SSID" password "$PASSWORD" &&
                    notify-send "Network Menu" "Connected to $SSID" ||
                    notify-send "Network Menu" "Failed to connect to $SSID"
            else
                notify-send "Network Menu" "No password entered"
            fi
        fi
    else
        notify-send "Network Menu" "No network selected"
    fi
}

view_ip_address() {
    IP=$(ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)
    if [ -n "$IP" ]; then
        notify-send "Network Menu" "IP Address: $IP"
    else
        notify-send "Network Menu" "No IP Address Found"
    fi
}

# Handle choices
case "$CHOICE" in
"${toggle_icon}  Toggle Wi-fi")
    toggle_wifi
    ;;
"直 Connect to Network")
    scan_and_connect
    ;;
"  View IP Address")
    view_ip_address
    ;;
"  Exit")
    exit 0
    ;;
esac
