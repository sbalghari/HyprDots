#!/bin/bash
#  _   _                  ____        _
# | | | |_   _ _ __  _ __|  _ \  ___ | |_ ___
# | |_| | | | | '_ \| '__| | | |/ _ \| __/ __|
# |  _  | |_| | |_) | |  | |_| | (_) | |_\__ \
# |_| |_|\__, | .__/|_|  |____/ \___/ \__|___/
#        |___/|_|
# By: Saifullah Balghari
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This script sets up HyprDots installer on your system.
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

set -e
cd ~

# Colors
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

## Paths
DOWNLOAD_DIR="$HOME/.cache/hyprdots"
LOG_FILE="$HOME/.cache/hyprdotsSetup.log"
METADATA_FILE="$HOME/.config/hyprdots/metadata.json"

# Source directories
SOURCE_LIB_DIR="$DOWNLOAD_DIR/lib"
SOURCE_BIN_DIR="$DOWNLOAD_DIR/bin"
SOURCE_SHARE_DIR="$DOWNLOAD_DIR/share"

# Target HyprDots directories
TARGET_LIB_DIR="/usr/lib/hyprdots"
TARGET_BIN_DIR="/usr/local/bin"
TARGET_SHARE_DIR="/usr/share/hyprdots"

# Main installer script
MAIN_INSTALLER="$TARGET_LIB_DIR/main.py"

# Create an empty log file
mkdir -p "$(dirname "$LOG_FILE")"
touch "$LOG_FILE"
: >$LOG_FILE

# Logger function
log() {
	local level=$1
	local message=$2
	local timestamp
	timestamp=$(date +"%Y-%m-%d %H:%M:%S")
	echo "[${timestamp}] [${level}] ${message}" >>"$LOG_FILE"
}

# Colored output helpers
info() { echo -e "${YELLOW}> $1${RESET}"; }
success() { echo -e "${GREEN}✔ $1${RESET}"; }
fail() { echo -e "${RED}✘ $1${RESET}"; }

generateMetadata() {
	local release_type="$1" # "stable" or "rolling"
	local repo_dir="$DOWNLOAD_DIR"
	local version=""
	local commit_full=""
	local commit_short=""
	local installed_at

	installed_at=$(date --iso-8601=seconds)

	commit_hash=$(git -C "$repo_dir" rev-parse --short HEAD)

	if [ "$release_type" = "stable" ]; then
		version=$(git -C "$repo_dir" describe --tags --abbrev=0)
	else
		local tag
		tag=$(git -C "$repo_dir" describe --tags --abbrev=0 2>/dev/null || echo "untagged")
		version="${tag}-${commit_hash}"
	fi

	# Make sure the metadata directory exists
	mkdir -p "$(dirname "$METADATA_FILE")"

	# Check if the metadata file already exists
	if [ -f "$METADATA_FILE" ]; then
		log "Info" "Metadata file already exists. Overwriting..."
		: >"$METADATA_FILE"

	# If the file doesn't exist, it will be created
	else
		log "Info" "Creating metadata file at $METADATA_FILE"
		touch "$METADATA_FILE"
	fi

	# Write metadata JSON
	sudo tee "$METADATA_FILE" >/dev/null <<EOF
{
  "release_type": "$release_type",
  "version": "$version",
  "installed_at": "$installed_at"
}
EOF

	log "Info" "Generated metadata at $METADATA_FILE"
	success "Saved metadata: $version"
}

# Function to copy files from a directory to another directory using rsync
copy() {
	local source_dir="$1"
	local target_dir="$2"

	if [[ ! -d "$source_dir" ]]; then
		fail "Source dir $source_dir does not exist."
		log "Error" "Source dir $source_dir does not exist."
		return 1
	fi

	log "Info" "Copying files from $source_dir to $target_dir."
	if gum spin --spinner dot --title "Copying..." \
		-- bash -c "
        sudo rsync -av \"$source_dir/\" \"$target_dir/\"
    "; then
		success "Copied files from $source_dir to $target_dir."
		log "Success" "Copied files from $source_dir to $target_dir."
		return 0 # True
	else
		fail "Could not copy files. Check $LOG_FILE."
		log "Error" "Could not copy files from $source_dir to $target_dir."
		return 1 # False
	fi
}

# Main Setup function
# This function will remove existing HyprDots directories, create new ones, and copy files to the target directories.
setup() {
	log "Info" "Removing existing HyprDots directories if they exist..."
	info "Removing existing HyprDots directories if they exist..."
	if remove_files_in_a_dir "$TARGET_BIN_DIR" &&
		remove_dir_if_exists "$TARGET_LIB_DIR" &&
		remove_dir_if_exists "$TARGET_SHARE_DIR"; then
		log "Success" "Removed existing HyprDots directories."
		success "Removed existing HyprDots directories."
	else
		log "Error" "Failed to remove one or more HyprDots directories."
		fail "Failed to remove one or more HyprDots directories."
		return 1 # False
	fi

	log "Info" "Creating target directories..."
	info "Creating target directories..."
	create_dir_if_not_exists "$TARGET_LIB_DIR"
	create_dir_if_not_exists "$TARGET_BIN_DIR"
	create_dir_if_not_exists "$TARGET_SHARE_DIR"
	log "Info" "Created target directories."

	# Copy files
	info "Copying files to target directories..."
	log "Info" "Copying files to target directories..."

	# Lib
	info "Installing libraries to $TARGET_LIB_DIR..."
	if copy "$SOURCE_LIB_DIR" "$TARGET_LIB_DIR"; then
		log "Success" "Installed libraries."
	else
		fail "Failed to Install libraries."
		return 1 # False
	fi

	# Bin
	info "Installing binaries to $TARGET_BIN_DIR..."
	if copy "$SOURCE_BIN_DIR" "$TARGET_BIN_DIR"; then
		log "Success" "Installed binaries."
	else
		fail "Failed to Install binaries."
		return 1 # False
	fi

	# Share
	info "Installing shared files to $TARGET_SHARE_DIR..."
	if copy "$SOURCE_SHARE_DIR" "$TARGET_SHARE_DIR"; then
		log "Success" "Installed shared files."
	else
		fail "Failed to Install shared files."
		return 1 # False
	fi

	return 0 # True
}

header() {
	clear
	figlet "HyprDots"
	echo -e "${GREEN}Welcome to the HyprDots Setup!${RESET}\n"
	log "Info" "Launched setup"
}

run_main_installer() {
	cd ~
	if python3 "$MAIN_INSTALLER"; then
		log "Success" "Main installer ran successfully."
	else
		fail "Failed to run the main installer."
		log "Error" "Failed to run the main installer."
		exit 1
	fi
}

main() {
	log "Info" "Starting the setup..."

	log "Info" "Installing setup dependencies..."
	if installDependencies; then
		log "Success" "Installed setup dependencies"
	else
		log "Error" "Couldn't install setup dependencies"
		exit 1
	fi

	log "Info" "Installing yay..."
	if installYay; then
		log "Success" "Installed yay"
	else
		log "Error" "Couldn't install yay"
		exit 1
	fi

	header

	if [[ -d "$DOWNLOAD_DIR" ]]; then
		echo
		log "Info" "HyprDots download dir already exists."
		log "Info" "Removing existing HyprDots download directory..."
		if rm -rf "$DOWNLOAD_DIR"; then
			success "Removed existing HyprDots download directory."
			log "Success" "Removed existing HyprDots download directory."
			header
		else
			fail "Failed to remove existing HyprDots download directory."
			log "Error" "Failed to remove existing HyprDots download directory."
			exit 1
		fi
	fi

	info "Choose a version to download."
	log "Info" "Prompting user to choose release version."
	choice=$(gum choose "Stable" "Rolling")

	case "$choice" in
	"Stable")
		downloadStableRelease
		;;
	"Rolling")
		downloadRollingRelease
		;;
	3*)
		fail "Invalid choice. Exiting."
		log "Error" "Invalid choice selected."
		exit 1
		;;
	esac

	log "Info" "Downloaded HyprDots release."

	# Copy files to target directories
	if setup; then
		log "Info" "Files copied successfully."
		success "HyprDots setup completed successfully!"

		# Generate metadata
		if [ "$choice" = "Stable" ]; then
			generateMetadata "stable"
		else
			generateMetadata "rolling"
		fi

		# Run main installer
		info "Launching main installer..."
		if run_main_installer; then
			success "Installation complete!"
		else
			fail "Main installer failed to run"
			exit 1
		fi

		# Ask for reboot
		if gum confirm "Do you want to reboot now?"; then
			log "Info" "Rebooting system..."
			success "Rebooting system..."
			sudo reboot
		fi
	else
		log "Error" "Setup failed."
		exit 1
	fi

	# Cleanup
	log "Info" "Cleaning up..."
	remove_dir_if_exists "$DOWNLOAD_DIR"
	log "Info" "Removed download directory."
}
main
