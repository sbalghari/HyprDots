# Utility functions for filesystem operations

import os
import shutil

from shared import logger

def remove(filepath):
    """Remove a file or directory at the specified path.
    Args:
        filepath (str): The path to the file or directory to remove.
    Returns:
        bool: True if the removal was successful, False otherwise.
    """
    try:
        if not os.path.exists(filepath):
            logger.info(f"{filepath} does not exist, nothing to remove.")
            return True
        if os.path.islink(filepath):
            os.unlink(filepath)
            logger.info(f"{filepath} removed successfully")
        elif os.path.isfile(filepath):
            os.remove(filepath)
            logger.info(f"{filepath} file removed successfully")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)
            logger.info(f"{filepath} folder removed successfully")
        else:
            logger.info(f"{filepath} does not exist")
    except OSError as e:
        logger.error(f"Error deleting {filepath}: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False
    return True

def check_configs_exists(filepath) -> bool:
    """Check if a configuration file exists at the specified path.
    Args:
        filepath (str): The path to the configuration file.
    Returns:
        bool: True if the file exists, False otherwise.
    """
    if not os.path.exists(filepath):
        logger.error(f"Missing config: {filepath}.")
        return False
    return True

def create_symlink(source, target) -> bool:
    """Create a symbolic link from source to target.
    Args:
        source (str): The source file or directory to link from.
        target (str): The target file or directory to link to.
    Returns:
        bool: True if the symlink was created successfully, False otherwise.
    """
    try:
        if os.path.lexists(target):
            os.unlink(target)
            logger.info(f"Removed existing target: {target}")

        os.symlink(source, target, target_is_directory=os.path.isdir(source))
        logger.info(f"Symlink created: {source} --> {target}")
        return True
    except Exception as e:
        logger.error(f"Error while linking: {source} --> {target}, Error: {e}")
        return False
