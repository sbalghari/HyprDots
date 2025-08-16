# Utility functions for operations on packages
from typing import List
import subprocess

from shared import logger

def install_package(package: str) -> bool:
    """ 
    Installs a package.
    
    Args:
        package (str): The name of the package to install.  
    
    Returns:
        bool: True if the package was installed successfully, False otherwise.
    """
    logger.info(f"Installing package: {package}")
    if is_installed(package):
        logger.info(f"Package {package} is already installed, Skipping...")
        return True
    
    result = run_command([
        "yay",
        "-S",
        f"{package}",
        "--noconfirm",
        "--quiet"
    ])
    
    if result.returncode != 0:
        logger.error(f"Unable to install package: {package}, Error: {result.stderr()}")
        return False
    return True

def install_package_group(group: List[str], group_name: str) -> bool:
    """ 
    Installs a group of packages.
    
    Args:
        group (List[str]): List of package names to install.
        group_name (str): Name of the package group for logging purposes.
   
    Returns:
        bool: True if all packages in the group were installed successfully, False otherwise.
    """
    logger.info(f"Installing {group_name}.")
    for package in group:
        if not install_package(package):
            logger.error(f"Couldn't install {package}.")
            return False
        
    logger.info(f"All {group_name} installed successfully.")
    return True

def is_installed(package: str) -> bool:
    """ 
    Check if a system package is installed.
    
    Args:
        package (str): The name of the package to check.
    
    Returns:
        bool: True if the package is installed, False otherwise.
    """
    result = subprocess.run(
        ["pacman", "-Qq", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def run_command(command: List[str]) -> subprocess.CompletedProcess:
    """ 
    Runs a shell command using subprocess.run
    
    Args:
        command (List[str]): The command to run as a list of strings.
    
    Returns:
        subprocess.CompletedProcess: The result of the command execution.
    
    Raises:
        ValueError: If the command is an empty list.
        FileNotFoundError: If the executable is not found.
        subprocess.CalledProcessError: If the command returns a non-zero exit code.
        RuntimeError: For other subprocess errors or unexpected errors.
    """
    if not isinstance(command, list) or not command:
        raise ValueError("Command must be a non-empty list of strings.")

    try:
        result = subprocess.run(
            command,
            text=True,
            check=True,
        )
        return result

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Executable not found: {command[0]}") from e

    except subprocess.CalledProcessError as e:
        err_msg = f"Command '{' '.join(command)}' failed with exit code {e.returncode}"
        err_msg += f"\nstdout: {e.stdout}\nstderr: {e.stderr}"
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, output=e.output, stderr=e.stderr
        ) from e

    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Subprocess error while executing: {' '.join(command)}\n{e}") from e

    except Exception as e:
        raise RuntimeError(f"Unexpected error while running command: {' '.join(command)}\n{e}") from e