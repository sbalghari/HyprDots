#!/usr/bin/env python3

import subprocess
import json
import sys

def get_active_window():
    try:
        # Get the active window information
        window_info = subprocess.run(
            ["hyprctl", "activewindow", "-j"],
            stdout=subprocess.PIPE, 
            text=True, 
            check=True
        )
        
        # Parse the JSON output
        window_info = json.loads(window_info.stdout)
        
        # Get the application and title
        application = window_info.get("class", "Unknown")
        title = window_info.get("title", "Unknown")
        
        # Check if the application and title is unknown
        if application == "Unknown" and title == "Unknown":
            return None
        
        # Map applications to icons
        icons = {
            "kitty": "",
            "Google-chrome": "󰊯",
            "Rofi": "󰵆",
            "discord": "",
            "Spotify": "󰓇",
            "Code": "",
            "waypaper": "󰸉",
            "net.lutris.Lutris": "",
            "vlc": "󰕼",
            "org.gnome.Nautilus": ""
        }
        
        # Get the icon for the application
        icon = icons.get(application, "")
        
        # Return the formatted output
        return f"{icon} {title}"
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not get active window - {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    text = get_active_window()
    if text:
        output = {
            "text": text,
            "tooltip": f"Active Window: {text}"
        }
    else:
        output = {
            "text": "",
            "tooltip": ""
        }
    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()