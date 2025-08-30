import subprocess
import shutil
import os
import sys
import logging
import json
from logging import Logger
from pathlib import Path
from time import sleep

# Directories
HYPRDOTS_DOWNLOADED_DIR = Path.home() / "HyprDots"
LIB_DIR = Path("/usr/lib/hyprdots")
BIN_DIR = Path("/usr/local/bin")
SHARE_DIR = Path("/usr/share/hyprdots")

# Log file
LOG_FILE = Path.home() / ".cache/hyprdots_setup.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    filemode="w"
)
log: Logger = logging.getLogger()

# Colors
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
RESET = "\033[0m"

# Colorful message functions
def info(msg: str) -> None:
    print(f"{YELLOW}> {msg}{RESET}")

def success(msg: str) -> None:
    print(f"{GREEN}✔ {msg}{RESET}")

def fail(msg: str) -> None:
    print(f"{RED}✘ {msg}{RESET}")

def generate_metadata() -> bool:
    """
    Generate metadata.json with installation details.
    Returns True if successful, False otherwise.
    """
    metadata_file = SHARE_DIR / "metadata.json"
    release_type_marker = HYPRDOTS_DOWNLOADED_DIR / "release_type.txt"
    repo_dir = HYPRDOTS_DOWNLOADED_DIR

    def _run_git_command(*args):
        """Run a git command and return its output."""
        try:
            return subprocess.check_output(
                ["git"] + list(args),
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            return None

    def _get_version() -> str:
        return _run_git_command("-C", str(repo_dir), "describe", "--tags", "--always", "--dirty")
    
    def _get_commit_hash() -> str:
        return _run_git_command("-C", str(repo_dir), "rev-parse", "HEAD")

    def _get_release_type() -> str:
        try:
            with open(release_type_marker, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            log.error("release_type.txt not found.")
            return None

    version = _get_version()
    commit_hash = _get_commit_hash()
    release_type = _get_release_type()

    if not all([version, commit_hash, release_type]):
        log.error("Failed to retrieve all metadata information.")
        return False

    metadata = {
        "version": version,
        "commit_hash": commit_hash,
        "release_type": release_type
    }
    
    log.debug(f"Generated metadata: {metadata}")

    try:
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)
        log.info(f"Metadata written to {metadata_file}")
        return True
    except PermissionError:
        log.warning(f"No permission to write {metadata_file}, retrying with sudo...")
        try:
            json_str = json.dumps(metadata, indent=4)
            subprocess.run(
                ["sudo", "tee", str(metadata_file)],
                input=json_str.encode(),
                check=True,
                stdout=subprocess.DEVNULL
            )
            log.info(f"Metadata written to {metadata_file} using sudo")
            return True
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to write metadata with sudo: {e}")
            return False
    except Exception as e:
        log.error(f"Failed to write metadata: {e}")
        return False

def copy(src: Path, dest: Path) -> bool:
    """
    Copy files or directories from src to dest.
    Automatically overwrites if dest exists.
    Falls back to sudo when needed.
    Returns True if successful, False otherwise.
    """
    try:
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
            log.info(f"Overwritten existing {dest} without sudo")

        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        log.info(f"Copied {src} to {dest} without sudo")
        return True

    except PermissionError:
        log.warning(f"Permission denied copying {src} to {dest}, retrying with sudo...")
        try:
            subprocess.run(
                ["sudo", "rm", "-rf", str(dest)],
                check=False
            )
            subprocess.run(
                ["sudo", "cp", "-r", str(src), str(dest)],
                check=True
            )
            log.info(f"Copied {src} to {dest} using sudo")
            return True
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to copy {src} to {dest} with sudo: {e}")
            return False

    except Exception as e:
        log.error(f"Unexpected error copying {src} to {dest}: {e}")
        return False

def setup() -> bool:
    """ Main function to setup HyprDots on the system. """
    if not HYPRDOTS_DOWNLOADED_DIR.exists():
        fail(f"Source directory {HYPRDOTS_DOWNLOADED_DIR} does not exist.")
        return False
    
    info("Copying files to system directories...")
    sleep(1)  # Small delay for better UX
    src = [HYPRDOTS_DOWNLOADED_DIR / "lib", HYPRDOTS_DOWNLOADED_DIR / "bin", HYPRDOTS_DOWNLOADED_DIR / "share"]
    dest = [LIB_DIR, BIN_DIR, SHARE_DIR]
    
    for s, d in zip(src, dest):
        if not copy(s, d):
            fail(f"Failed to copy {s} to {d}. Aborting setup.")
            return False
    success("All files copied successfully.")
    print()
    
    info("Genarating metadata...")
    sleep(1)  # Small delay for better UX
    if not generate_metadata():
        fail("Failed to generate metadata. Aborting setup.")
        return False
    success("Metadata generated successfully.")
    print()
    
    return True

def main() -> None:
    log.info("Starting HyprDots setup...")
    print()
    if setup():
        success("HyprDots setup completed successfully!")
    else:
        fail("HyprDots setup failed. Check the log file for details.")
        sys.exit(1)
        
    print()
    log.info("Launching HyprDots...")
    os.system("gum spin --title \"Launching HyprDots...\" -- sleep 2")
    
if __name__ == "__main__":
    main()
    