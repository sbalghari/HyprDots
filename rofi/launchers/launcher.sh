#!/usr/bin/env bash

## Author : Aditya Shakya (adi1090x)
## Github : @adi1090x
#
## Rofi   : Launcher (Modi Drun, Run, File Browser, Window)

theme="$HOME"/.config/rofi/launchers/style-2

## Run
rofi \
    -show drun \
    -theme ${theme}.rasi
