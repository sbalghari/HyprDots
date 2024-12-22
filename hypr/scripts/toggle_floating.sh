#!/bin/bash

# Modified by:  Saifullah Balghari
# Original:     Stephen Raabe (ML4W)

floating=$(hyprctl activewindow -j | jq '.floating')
window=$(hyprctl activewindow -j | jq '.initialClass' | tr -d "\"")

function toggle() {
  width=$1
  height=$2

  hyprctl --batch "dispatch togglefloating; dispatch resizeactive exact ${width} ${height}; dispatch centerwindow"
}

function untoggle() {
  hyprctl dispatch togglefloating
}

function handle() {
  width=$1
  height=$2

  if [ "$floating" == "false" ]; then
    toggle "$width" "$height"
  else
    untoggle
  fi
}

case $window in
kitty) handle "50%" "55%" ;;
*) handle "70%" "70%" ;;
esac
