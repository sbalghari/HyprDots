#!/bin/bash

# By:  Saifullah Balghari

if [[ -z "$1" ]]; then
    echo "No arguments passed."
    echo "Usage: $0 <change|restore|help>"
    exit 1
fi

if [[ $1 == "change" ]]; then
    waypaper --random &
elif [[ $1 == "restore" ]]; then
    waypaper --restore
else
    echo "No args passed"
fi