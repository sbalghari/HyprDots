import subprocess


def reload_hyprland() -> bool:
    result = subprocess.run(
        ["hyprctl", "reload"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0
