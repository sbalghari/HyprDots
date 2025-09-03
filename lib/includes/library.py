import shutil
from pathlib import Path
from typing import List
import json
import subprocess

from .logger import logger
from .paths import HYPRDOTS_METADATA_FILE


def get_version() -> str:
    """Get the current version of HyprDots from metadata file."""
    try:
        with open(HYPRDOTS_METADATA_FILE, "r") as f:
            metadata = json.load(f)
            return metadata.get("version", "unknown")
    except Exception:
        return "unknown"


def path_lexists(path: Path) -> bool:
    """True for existing paths or broken symlinks."""
    return path.exists() or path.is_symlink()


def remove(filepath: Path) -> bool:
    """Remove a file, directory, or symlink at the given path."""
    try:
        if not path_lexists(filepath):
            logger.info(f"{filepath} does not exist, nothing to remove.")
            return True

        if filepath.is_symlink() or filepath.is_file():
            filepath.unlink()
            logger.info(f"{filepath} removed successfully")
        elif filepath.is_dir():
            shutil.rmtree(filepath)
            logger.info(f"{filepath} directory removed successfully")
    except OSError as e:
        logger.error(f"Error deleting {filepath}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error removing {filepath}: {e}")
        return False
    return True


def check_configs_exists(filepath: Path) -> bool:
    """Check if a config file exists or is a symlink."""
    if not path_lexists(filepath):
        logger.error(f"Missing config: {filepath}.")
        return False
    return True


def create_symlink(source: Path, target: Path) -> bool:
    """Create or replace a symlink from source → target."""
    try:
        if path_lexists(target):
            if target.is_symlink() or target.is_file():
                target.unlink()
            elif target.is_dir():
                shutil.rmtree(target)
            logger.info(f"Removed existing target: {target}")

        target.symlink_to(source, target_is_directory=source.is_dir())
        logger.info(f"Symlink created: {source} --> {target}")
        return True
    except Exception as e:
        logger.error(f"Error while linking {source} --> {target}: {e}")
        return False


def is_installed(package: str) -> bool:
    """Check if a package is installed with pacman."""
    result = subprocess.run(
        ["pacman", "-Qq", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def run_command(command: List[str], check: bool = False) -> subprocess.CompletedProcess:
    """Run a command safely and return its result."""
    if not command:
        raise ValueError("Command must be a non-empty list of strings.")
    try:
        return subprocess.run(command, text=True, capture_output=True, check=check)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Executable not found: {command[0]}") from e
    except subprocess.SubprocessError as e:
        raise RuntimeError(
            f"Subprocess error: {' '.join(command)}\n{e}") from e
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error: {' '.join(command)}\n{e}") from e


def install_package(package: str) -> bool:
    """Install a package with yay if not already installed."""
    logger.info(f"Installing package: {package}")
    if is_installed(package):
        logger.info(f"Package {package} is already installed, skipping.")
        return True
    try:
        result = run_command(
            ["yay", "-S", package, "--noconfirm", "--quiet"], check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Unable to install {package}. Exit code {e.returncode}.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error installing {package}: {e}")
        return False


def install_package_group(group: List[str], group_name: str) -> bool:
    """Install a list of packages."""
    logger.info(f"Installing {group_name}.")
    for package in group:
        if not install_package(package):
            logger.error(f"Failed to install {package}.")
            return False
    logger.info(f"All {group_name} installed successfully.")
    return True
