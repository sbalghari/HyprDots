#  _     _ _
# | |   (_) |__  _ __ __ _ _ __ _   _
# | |   | | '_ \| '__/ _` | '__| | | |
# | |___| | |_) | | | (_| | |  | |_| |
# |_____|_|_.__/|_|  \__,_|_|   \__, |
#                               |___/
# # # # # # # # # # # # # # # # # # # # # # # #
# Collection of utility functions for SBDots
# # # # # # # # # # # # # # # # # # # # # # # #

from pathlib import Path
from typing import List, Optional, Union
import json
import shutil
import subprocess
import threading
import time
import atexit

from .logger import logger
from .paths import SBDOTS_METADATA_FILE


def get_version() -> str:
    """Get the current version of SBDots from metadata file."""
    try:
        with open(SBDOTS_METADATA_FILE, "r") as f:
            metadata = json.load(f)
            return metadata.get("version", "unknown")
    except Exception as e:
        logger.error(f"Failed to read version metadata: {e}")
        return "unknown"


#  ____            _
# / ___| _   _ ___| |_ ___ _ __ ___
# \___ \| | | / __| __/ _ \ '_ ` _ \
#  ___) | |_| \__ \ ||  __/ | | | | |
# |____/ \__, |___/\__\___|_| |_| |_|
#        |___/
# # # # # # # # # # # # # # # # # # #

def run_command(command: List[Union[str, Path]]) -> subprocess.CompletedProcess:
    """Run a command safely and return its result."""
    if not command:
        raise ValueError("Command must be a non-empty list of strings.")

    # Convert Path objects to strings
    str_command = [str(arg) if isinstance(arg, Path)
                   else arg for arg in command]

    try:
        return subprocess.run(str_command, text=True, capture_output=True)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Executable not found: {command[0]}") from e
    except subprocess.SubprocessError as e:
        raise RuntimeError(
            f"Subprocess error: {' '.join(str_command)}\n{e}") from e
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(
            f"Command took too long to execute: {' '.join(str_command)}\n{e}") from e
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error: {' '.join(str_command)}\n{e}") from e


def is_vm() -> bool:
    """Detect if the system is a VM using DMI information"""

    dmi_path = Path("/sys/class/dmi/id")

    vm_signatures = [
        "vmware", "virtualbox", "innotek gmbh", "kvm", "qemu",
        "xen", "microsoft corporation", "virtual machine",
        "amazon ec2", "google compute engine"
    ]

    for field in ["product_name", "sys_vendor", "bios_vendor"]:
        file_path = dmi_path / field
        if file_path.exists():
            try:
                content = file_path.read_text().strip().lower()
                if any(sig in content for sig in vm_signatures):
                    return True
            except (IOError, PermissionError):
                continue

    return False


def is_laptop() -> bool:
    """Detect if the system is a laptop or desktop on Linux systems"""

    battery_dir = Path("/sys/class/power_supply")
    battery_found = False
    ac_power_found = False

    try:
        if not battery_dir.is_dir():
            logger.debug("Power supply directory not found")
            return False

        for entry in battery_dir.iterdir():
            if not entry.is_dir():
                continue

            name = entry.name.upper()

            # Check for battery devices
            if name.startswith("BAT"):
                # Check if it has capacity file
                capacity_file = entry / "capacity"
                if capacity_file.exists():
                    battery_found = True
                    logger.debug(f"Found battery: {entry.name}")

            # Check for AC power (common on laptops)
            elif name.startswith(("AC", "ADP")):
                ac_power_found = True
                logger.debug(f"Found AC power supply: {entry.name}")

        # Consider it a laptop if we found a battery with capacity info
        # or if we found both battery and AC power
        return battery_found or (ac_power_found and any(
            e.name.upper().startswith("BAT") for e in battery_dir.iterdir()
            if e.is_dir()
        ))

    except PermissionError:
        logger.warning(
            "Permission denied accessing power supply information")
        return False
    except Exception as e:
        logger.error(f"Unexpected error detecting laptop: {e}")
        return False


class SudoKeepAlive:
    def __init__(self, max_duration: Optional[int] = None):
        """
        Initialize sudo keep-alive.

        Args:
            interval: Seconds between sudo validations (default: 60)
            max_duration: Maximum duration in seconds before auto-stop (optional)
        """
        self.interval = 60
        self.max_duration = max_duration
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._is_running = False
        self._start_time: Optional[float] = None

    def start(self) -> None:
        """Ask for sudo once, then keep it alive in background."""
        with self._lock:
            if self._is_running:
                return  # Already running

            try:
                subprocess.run(
                    ["sudo", "-v"],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Failed to obtain sudo privileges: {e.stderr}")

            self._is_running = True
            self._start_time = time.time()
            self._stop.clear()
            self._thread = threading.Thread(
                target=self._keepalive, daemon=True)
            self._thread.start()
            atexit.register(self.stop)

    def _keepalive(self) -> None:
        """Background thread to maintain sudo privileges."""
        while not self._stop.is_set():
            time.sleep(self.interval)

            # Check if max duration has been exceeded
            if (self.max_duration is not None and
                self._start_time is not None and
                    time.time() - self._start_time > self.max_duration):
                self.stop()
                break

            try:
                subprocess.run(
                    ["sudo", "-v"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            except subprocess.CalledProcessError:
                # Sudo authentication failed, stop the thread
                self._stop.set()
                break

    def stop(self) -> None:
        """Stop keepalive and invalidate sudo timestamp."""
        with self._lock:
            if not self._is_running:
                return

            self._stop.set()
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=1.0)

            subprocess.run(
                ["sudo", "-k"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self._is_running = False
            self._start_time = None
            atexit.unregister(self.stop)

    @property
    def is_running(self) -> bool:
        """Return whether the keepalive is active."""
        with self._lock:
            return self._is_running

    @property
    def elapsed_time(self) -> Optional[float]:
        """Return elapsed time since start in seconds, or None if not running."""
        with self._lock:
            if self._is_running and self._start_time:
                return time.time() - self._start_time
            return None

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def restart(self) -> None:
        """Restart the keepalive mechanism."""
        self.stop()
        time.sleep(0.1)  # Brief pause
        self.start()


#   __ _ _                                   _   _
#  / _(_) | ___     ___  _ __   ___ _ __ __ _| |_(_) ___  _ __  ___
# | |_| | |/ _ \   / _ \| '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \/ __|
# |  _| | |  __/  | (_) | |_) |  __/ | | (_| | |_| | (_) | | | \__ \
# |_| |_|_|\___|   \___/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|___/
#                      |_|
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def path_lexists(path: Path) -> bool:
    """Check for existing paths or broken symlinks."""
    return path.exists() or path.is_symlink()


def copy(src: Path, dest: Path) -> bool:
    """
    Safely copy files or directories from src to dest.
    Automatically overwrites if dest exists. Falls back to sudo when needed.
    """
    try:
        # Validate source exists
        if not src.exists():
            logger.error(f"Source path does not exist: {src}")
            return False

        # Ensure parent dir exists
        if not _create_parent_dir(dest):
            logger.error(f"Failed to create parent directory: {dest.parent}")
            return False

        # Remove dest if exists
        if dest.exists():
            logger.info(f"Destination already exists, removing: {dest}")
            if not remove(dest):
                logger.error(f"Failed to remove destination: {dest}")
                return False

        if _copy_without_sudo(src, dest):
            return True
        if _copy_with_sudo(src, dest):
            return True

        logger.error(f"All copy attempts failed: {src} -> {dest}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during copy: {src} -> {dest}: {e}")
        return False


def _create_parent_dir(path: Path) -> bool:
    parent_dir = path.parent
    if parent_dir.exists():
        return True

    result = run_command(["sudo", "mkdir", "-p", parent_dir])
    if result.returncode == 0:
        logger.info(f"Created parent directory: {parent_dir}")
        return True
    else:
        logger.error(
            f"Failed to create parent directory: {parent_dir}: {result.stderr}")
        return False


def _copy_without_sudo(src: Path, dest: Path) -> bool:
    try:
        if src.is_dir():
            shutil.copytree(src, dest, symlinks=True, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)

        logger.info(f"Copied successfully without sudo: {src} -> {dest}")
        return True

    except (PermissionError, OSError) as e:
        logger.warning(
            f"Permission denied copying without sudo: {src} -> {dest}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error copying without sudo: {src} -> {dest}: {e}")
        return False


def _copy_with_sudo(src: Path, dest: Path) -> bool:
    try:
        if src.is_dir():
            cp_cmd = ["sudo", "cp", "-r", src, dest]
        else:
            cp_cmd = ["sudo", "cp", "--preserve=all", src, dest]

        result = run_command(cp_cmd)
        if result.returncode == 0:
            logger.info(f"Copied successfully with sudo: {src} -> {dest}")
            return True
        else:
            logger.error(
                f"Failed to copy with sudo: {src} -> {dest}: {result.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed during sudo copy: {src} -> {dest}: {e}")
        return False
    except Exception as e:
        logger.error(
            f"Unexpected error during sudo copy: {src} -> {dest}: {e}")
        return False


def remove(filepath: Path) -> bool:
    """
    Remove a file, directory, or symlink at the given path.
    Falls back to sudo when needed.
    """
    # Return if filepath doesn't exist
    if not path_lexists(filepath):
        logger.info(f"Path does not exist, nothing to remove: {filepath}")
        return True

    try:
        if filepath.is_symlink() or filepath.is_file():
            filepath.unlink()
        elif filepath.is_dir():
            shutil.rmtree(filepath)

        logger.info(f"Removed successfully: {filepath}")
        return True

    # If any error occurs, try with sudo
    except (PermissionError, OSError, Exception) as e:
        logger.warning(
            f"Error removing path: {filepath}: {e}. Retrying with sudo...")

        try:
            result = run_command(["sudo", "rm", "-rf", filepath])
            if result.returncode == 0:
                logger.info(f"Removed successfully with sudo: {filepath}")
                return True
            else:
                logger.error(
                    f"Failed to remove with sudo: {filepath}: {result.stderr}")
                return False

        except subprocess.CalledProcessError as e:
            logger.error(
                f"Command failed during sudo removal: {filepath}: {e}")
            return False
        except Exception as e:
            logger.error(
                f"Unexpected error during sudo removal: {filepath}: {e}")
            return False


def create_symlink(source: Path, target: Path) -> bool:
    """Create or replace a symlink from source → target."""
    try:
        # Remove target if exists
        if not remove(target):
            logger.error(f"Failed to remove target: {target}")
            return False

        # Create symlink
        target.symlink_to(source, target_is_directory=source.is_dir())
        logger.info(f"Symlink created: {source} -> {target}")
        return True
    except Exception as e:
        logger.error(f"Error creating symlink: {source} -> {target}: {e}")
        return False


#  ____            _
# |  _ \ __ _  ___| | ____ _  __ _  ___  ___
# | |_) / _` |/ __| |/ / _` |/ _` |/ _ \/ __|
# |  __/ (_| | (__|   < (_| | (_| |  __/\__ \
# |_|   \__,_|\___|_|\_\__,_|\__, |\___||___/
#                            |___/
# # # # # # # # # # # # # # # # # # # # # # #

def is_installed(package: str) -> bool:
    """Check if a package is installed using pacman."""
    result = run_command(["pacman", "-Qq", package])
    return result.returncode == 0


def install_package(package: str) -> bool:
    """Install a package with yay."""
    logger.info(f"Installing package: {package}")

    # Check if package is installed or not
    if is_installed(package):
        logger.info(f"Package already installed, skipping: {package}")
        return True

    try:
        result = run_command(
            ["yay", "-S", package, "--noconfirm", "--quiet"]
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to install package: {package}. Exit code: {e.returncode}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error installing package: {package}: {e}")
        return False


def install_package_group(group: List[str], group_name: str) -> bool:
    """Install a list of packages. Continues through failures, returns False if any fail."""
    logger.info(f"Installing package group: {group_name}")
    failed = []

    for package in group:
        if not install_package(package):
            logger.error(f"Failed to install package: {package}")
            failed.append(package)

    if failed:
        logger.error(
            f"Some packages failed in group: {group_name}: {', '.join(failed)}")
        return False

    logger.info(f"All packages installed successfully in group: {group_name}")
    return True


def remove_package(package: str) -> bool:
    """Uninstall a package"""
    logger.info(f"Uninstalling package: {package}")

    # Check if package is installed or not
    if not is_installed(package):
        logger.info(f"Package not installed, skipping: {package}")
        return True

    try:
        result = run_command(
            ["yay", "-R", package, "--noconfirm", "--quiet"]
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to uninstall package: {package}. Exit code: {e.returncode}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error uninstalling package: {package}: {e}")
        return False
