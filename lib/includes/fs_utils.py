# Utility functions for filesystem operations

import shutil
from pathlib import Path
from shared import logger

def path_lexists(path: Path) -> bool:
    """
    Equivalent to os.path.lexists() using pathlib.
    Returns True for existing files/dirs and for broken symlinks.
    """
    return path.exists() or path.is_symlink()

def remove(filepath: Path) -> bool:
    """
    Remove a file, directory, or symlink at the specified path.
    
    Args:
        filepath (Path): The path to remove.
    
    Returns:
        bool: True if the removal was successful, False otherwise.
    """
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
        logger.error(f"An unexpected error occurred: {e}")
        return False
    return True

def check_configs_exists(filepath: Path) -> bool:
    """
    Check if a configuration file exists at the specified path.
    
    Args:
        filepath (Path): The path to the configuration file.
    
    Returns:
        bool: True if the file exists (or is a symlink), False otherwise.
    """
    if not path_lexists(filepath):
        logger.error(f"Missing config: {filepath}.")
        return False
    return True

def create_symlink(source: Path, target: Path) -> bool:
    """
    Create a symbolic link from source to target, replacing any existing link/file/dir.
    
    Args:
        source (Path): The source file or directory to link from.
        target (Path): The target file or directory to link to.
    
    Returns:
        bool: True if the symlink was created successfully, False otherwise.
    """
    try:
        if path_lexists(target):
            target.unlink()
            logger.info(f"Removed existing target: {target}")

        target.symlink_to(source, target_is_directory=source.is_dir())
        logger.info(f"Symlink created: {source} --> {target}")
        return True
    except Exception as e:
        logger.error(f"Error while linking: {source} --> {target}, Error: {e}")
        return False
