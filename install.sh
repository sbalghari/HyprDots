#!/bin/bash

# Function to display messages
function display_message {
    echo ">>> $1"
}

# Install dependencies using yay
display_message "Installing dependencies..."
yay -S --needed - < Dependencies

# Check if the installation was successful
if [ $? -eq 0 ]; then
    display_message "Dependencies installed successfully."
else
    display_message "Failed to install dependencies."
    exit 1
fi

# Copy configuration
display_message "Copying configuration files..."
cp -r configs/* ~/.config/

# Check if the copy was successful
if [ $? -eq 0 ]; then
    display_message "Configuration files copied successfully."
else
    display_message "Failed to copy configuration files."
    exit 1
fi

display_message "Script completed."
