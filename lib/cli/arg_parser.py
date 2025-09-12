import argparse
from includes.library import get_version


class ArgumentParser:
    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="HyprDots, a polished, feature-rich dotfiles for Arch Linux and Hyprland.",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "-i",
            "--install",
            action="store_true",
            help="Installs HyprDots on your system",
        )
        parser.add_argument(
            "-r",
            "--remove",
            action="store_true",
            help="Uninstalls HyprDots from your system",
        )
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Updates HyprDots to the latest version",
        )
        parser.add_argument(
            "-cu",
            "--check-update",
            action="store_true",
            help="Checks if a new version of HyprDots is available",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=get_version(),
            help="Show program version and exit",
        )

        return parser
