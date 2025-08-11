#!/bin/bash

# Paths
WALLPAPER_PATH="$1"
PYWAL_COLORS_CSS="$HOME/.cache/wal/colors.css"
HYPRLAND_COLORS_CONF="$HOME/.config/hypr/configs/colors.conf"

# Generate pywal colors
generate_pywal_colors() {
    local wallpaper_path=$1
    
    echo "[Debug]::Generating pywal colors"
    wal -i "$wallpaper_path" || { echo "[Error]::Failed to generate pywal colors"; exit 1; }
}

# Hex to ARGB conversion function
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
    magick "$input_image" -blur 0x30 "$output_image" || { echo "[Error]::Failed to blur image"; exit 1; }
}

# Store the blurred wallpaper
store_blurred_wallpaper() {
    local wallpaper_path=$1
    local cache_dir="$HOME/.cache/wallpaper"
    local blurred_image="$cache_dir/blurred_wallpaper.jpg"

    # Create the cache directory if it doesn't exist
    mkdir -p "$cache_dir"

    # Blur the wallpaper and store it in the cache directory
    blur_image "$wallpaper_path" "$blurred_image"
}

# Update hyprland window border colors
update_hyprland_colors() {
    # Parse pywal colors
    echo "[Debug]::Parsing pywal colors"
    fg_hex=$(grep -oP '(?<=--color11: )#[0-9a-fA-F]+' "$PYWAL_COLORS_CSS") || { echo "[Error]::Failed to parse fg color"; exit 1; }
    bg_hex=$(grep -oP '(?<=--color0: )#[0-9a-fA-F]+' "$PYWAL_COLORS_CSS") || { echo "[Error]::Failed to parse bg color"; exit 1; }

    # Convert hex colors to ARGB
    echo "[Debug]::Converting hex colors to ARGB"
    fg=$(hex_to_argb "$fg_hex")
    bg=$(hex_to_argb "$bg_hex")
    echo "[Info]::Foreground color: $fg"
    echo "[Info]::Background color: $bg"

    # Update colors.conf
    echo "[Debug]::Updating colors.conf"
    if [[ -n $fg && -n $bg ]]; then
        : > "$HYPRLAND_COLORS_CONF"
        echo "\$fg = $fg" >> "$HYPRLAND_COLORS_CONF"
        echo "\$bg = $bg" >> "$HYPRLAND_COLORS_CONF"
    else
        echo "[Error]::Could not extract or convert colors."
        exit 1
    fi
}

# Reload services
reload_services() {
    # Reload waybar
    echo "[Debug]::Reloading waybar"
    bash ~/.config/hypr/services/waybar.sh -r || { echo "[Error]::Failed to reload waybar"; exit 1; }

    # Reload swaync
    echo "[Debug]::Reloading swaync"
    bash ~/.config/hypr/services/swaync.sh -r || { echo "[Error]::Failed to reload swaync"; exit 1; }

    # Reload hyprland
    echo "[Debug]::Reloading hyprland"
    hyprctl reload || { echo "[Error]::Failed to reload hyprland"; exit 1; }
}

# Main
if [[ -n $WALLPAPER_PATH ]]; then
    generate_pywal_colors "$WALLPAPER_PATH"
    sleep 0.4
    update_hyprland_colors
    sleep 0.2
    reload_services
    store_blurred_wallpaper "$WALLPAPER_PATH"
    echo "[Success]::Wallpaper changed successfully."
else
    echo "[Error]::No wallpaper path provided."
    exit 1
fi

exit 0