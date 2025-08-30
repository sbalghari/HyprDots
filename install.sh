#!/bin/bash

# Download dir
DOWNLOAD_DIR="$HOME/.cache/hyprdots"

# Main setup script
SETUP="$DOWNLOAD_DIR/setup/setup.py"

# Colors
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

# Colored output helpers
info() { echo -e "${YELLOW}> $1${RESET}"; }
success() { echo -e "${GREEN}✔ $1${RESET}"; }
fail() { echo -e "${RED}✘ $1${RESET}"; }

# Function to check if a package is installed
_is_installed() {
	local package="$1"
	pacman -Q "$package" >/dev/null
}

# Function to install required dependencies of the setup script
_install_dependencies() {
	local deps=(curl gum figlet python-pyfiglet python-rich)

	info "Installing required dependencies..."
	echo && sleep 2
	for dep in "${deps[@]}"; do
		if ! _is_installed "$dep"; then
			if ! sudo pacman -S --noconfirm "$dep" >/dev/null 2>&1; then
				fail "Failed to install $dep."
				exit 1
			fi
		else
			info "$dep is already installed. Skipping..."
		fi
	done
}

# Function to install yay (AUR helper)
_install_yay() {
	if ! command -v yay &>/dev/null; then
		if gum spin --spinner dot --title "Installing yay..." \
			-- bash -c "
                git clone https://aur.archlinux.org/yay.git /tmp/yay &&
                cd /tmp/yay &&
                makepkg -si --noconfirm 
            "; then
			rm -rf /tmp/yay
			success "yay installed successfully."
		else
			fail "Failed to install yay. Check $LOG_FILE."
			exit 1
		fi
	else
		info "yay already installed. Skipping..."
	fi
}

_create_download_dir() {
	if [[ ! -d "$DOWNLOAD_DIR" ]]; then
		mkdir -p "$DOWNLOAD_DIR"
	else
		rm -rf "$DOWNLOAD_DIR"
		mkdir -p "$DOWNLOAD_DIR"
	fi
}

# Function to download the stable release of HyprDots
_download_stable_release() {
	info "Fetching latest stable release..."

	latest_tag=$(curl -s https://api.github.com/repos/sbalghari/HyprDots/releases |
		grep -B10 '"prerelease": true' |
		grep '"tag_name":' |
		head -n 1 |
		cut -d '"' -f4)

	if [[ -z "$latest_tag" ]]; then
		fail "Failed to fetch latest stable release tag."
		exit 1
	fi
	echo
	success "Fetched version: $latest_tag"

	_create_download_dir

	if gum spin --spinner dot --title "Cloning stable release $latest_tag..." \
		-- bash -c "git clone --branch \"$latest_tag\" --depth 1 https://github.com/sbalghari/HyprDots.git \"$DOWNLOAD_DIR\""; then
		success "Successfully cloned stable release $latest_tag"
	else
		fail "Failed to clone stable release. Retry later!"
		exit 1
	fi
}

# Function to download the rolling release of HyprDots
_download_rolling_release() {
	_create_download_dir

	if gum spin --spinner dot --title "Cloning rolling release..." \
		-- bash -c "git clone https://github.com/sbalghari/HyprDots.git \"$DOWNLOAD_DIR\""; then
		success "Successfully cloned rolling release"
	else
		fail "Failed to clone rolling release. Retry later!"
		exit 1
	fi
}

# Function to run the actual setup
_run_setup() {
	cd ~
	if ! python3 "$SETUP"; then
		fail "Failed to run the main setup."
		exit 1
	fi
}

main() {
	if _install_dependencies; then
		success "Installed setup dependencies"
		echo
	fi

	if _install_yay; then
		success "Installed yay (AUR helper)"
		echo
	fi

	info "Choose a version to download."
	choice=$(gum choose "Stable" "Rolling")

	case "$choice" in
	"Stable")
		_download_stable_release
		;;
	"Rolling")
		_download_rolling_release
		;;
	*)
		fail "Invalid choice. Exiting."
		exit 1
		;;
	esac

	# Create a marker of release type
	if [[ "$choice" == "Stable" ]]; then
		echo "stable" >"$DOWNLOAD_DIR/release_type.txt"
	else
		echo "rolling" >"$DOWNLOAD_DIR/release_type.txt"
	fi

	# Check if setup script exists
	if [[ ! -f "$SETUP" ]]; then
		echo
		fail "Setup script not found at $SETUP, something went wrong!"
		exit 1
	fi

	if ! _run_setup; then
		fail "Main setup failed to run, manually run $SETUP"
		exit 1
	fi
}

main
