#!/bin/bash

# Paths
WALLPAPER_PATH="$1"
PYWAL_COLORS_CSS="$HOME/.cache/wal/colors.css"
HYPRLAND_COLORS_CONF="$HOME/.config/hypr/configs/colors.conf"

# Generate pywal colors
generate_pywal_colors(){
    local wallpaper_path=$1
    
    echo "[Debug]::Generating pywal colors"
    wal -i "$wallpaper_path"
}

# hex to argb conversion function
hex_to_argb() {
    local hex="$1"
    local alpha="b3"
    local rr="${hex:1:2}"
    local gg="${hex:3:2}"
    local bb="${hex:5:2}"
    echo "0x${alpha}${rr}${gg}${bb}"
}

# Function to blur an image using ImageMagick
blur_image() {
    local input_image="$1"
    local output_image="$2"
    magick "$input_image" -blur 0x30 "$output_image"
}

# Store the blurred wallpaper in the cache directory
store_blurred_wallpaper() {
    local wallpaper_path=$1
    local cache_dir="$HOME/.cache/wallpaper"
    local blurred_image="$cache_dir/blurred_wallpaper.jpg"

    # Create the cache directory if it doesn't exist
    mkdir -p "$cache_dir"

    # Blur the wallpaper and store it in the cache
    blur_image "$wallpaper_path" "$blurred_image"
}

# Update hyprland window border colors
update_hyprland_colors(){
    # Parse pywal colors
    echo "[Debug]::Parsing pywal colors"
    fg_hex=$(grep -oP '(?<=--color11: )#[0-9a-fA-F]+' "$WAL_CSS")
    bg_hex=$(grep -oP '(?<=--color0: )#[0-9a-fA-F]+' "$WAL_CSS")

    # Convert hex colors to ARGB
    echo "[Debug]::Converting hex colors to ARGB"
    fg=$(hex_to_argb "$fg_hex")
    bg=$(hex_to_argb "$bg_hex")
    echo "[Info]::$fg"
    echo "[Info]::$bg"

    # Update colors.conf
    echo "[Debug]::Updating colors.conf"
    if [[ -n $fg && -n $bg ]]; then
        : > $COLORS_CONF
        echo "\$fg = $fg" >> $COLORS_CONF
        echo "\$bg = $bg" >> $COLORS_CONF
    else
        echo "[Error]:: Could not extract or convert colors."
    fi
}

# Reload services
reload_services(){
    # Reload waybar
    echo "[Debug]::Reloading waybar"
    bash ~/.config/hypr/services/waybar.sh -r
    sleep 0.2

    # Reload swaync
    echo "[Debug]::Reloading swaync"
    bash ~/.config/hypr/services/swaync.sh -r
    sleep 0.2

    # Reload nwg_dock
    echo "[Debug]::Reloading nwg_dock"
    bash ~/.config/hypr/services/nwg_dock.sh -r
    sleep 0.2

    # Reload hyprland
    echo "[Debug]::Reloading hyprland"
    hyprctl reload
}

# Main
if [[ -n $WALLPAPER_PATH ]]; then
    generate_pywal_colors "$WALLPAPER_PATH"
    sleep 0.2
    update_hyprland_colors
    sleep 0.1
    reload_services
    sleep 0.5
    store_blurred_wallpaper "$WALLPAPER_PATH"
    echo "[Success]::Wallpaper changed successfully."
else
    echo "[Error]::No wallpaper path provided."
fi