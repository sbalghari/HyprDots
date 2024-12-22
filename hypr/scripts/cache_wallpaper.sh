#!/bin/bash

# By:  Saifullah Balghari

path="$1"

# Function to blur an image using ImageMagick
blur_image() {
    local input_image="$1"
    local output_image="$2"
    magick "$input_image" -blur 0x10 "$output_image"
}

# Function to store the blurred wallpaper in the cache directory
store_blurred_wallpaper() {
    local wallpaper_path=$1
    local cache_dir="$HOME/.cache/hyprland/wallpapers"
    local blurred_image="$cache_dir/blurred_wallpaper.jpg"

    # Create the cache directory if it doesn't exist
    mkdir -p "$cache_dir"

    # Blur the wallpaper and store it in the cache
    blur_image "$wallpaper_path" "$blurred_image"
}

store_blurred_wallpaper "$path"
