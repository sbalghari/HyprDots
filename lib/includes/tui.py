import subprocess
import threading
import time
from typing import Optional, Callable
from rich.text import Text as RichText
from rich.live import Live as RichLive
from rich.spinner import Spinner as RichSpinner
from rich.style import Style as RichStyle
from rich.console import Console
from rich.prompt import Prompt

from functools import partial
from pyfiglet import figlet_format
from typing import List

from .logger import logger

# Colors
HEADER_COLOR: str = "#89b4fa"
PRIMARY_COLOR: str = "#cdd6f4"
ERROR_COLOR: str = "#f38ba8"
SUCCESS_COLOR: str = "#a6e3a1"
WARNING_COLOR: str = "#f9e2af"

# Characters
DONE_ICON: str = "✔"
WARNING_ICON: str = "⚠"
ERROR_ICON: str = "✖"
INFO_ICON: str = ">"

# Styles
HEADING_STYLE = RichStyle(color=HEADER_COLOR, bold=True)
_STYLE: partial = partial(RichStyle, bold=True, italic=True)
TEXT_STYLE = _STYLE(color=PRIMARY_COLOR)
SUBTEXT_STYLE = _STYLE(color="#bac2de", dim=True)
ERROR_STYLE = _STYLE(color=ERROR_COLOR)
SUCCES_STYLE = _STYLE(color=SUCCESS_COLOR)
WARNING_STYLE = _STYLE(color=WARNING_COLOR)


class Spinner:
    """Context manager for showing a live console spinner using `rich`.

    Enhanced with optional sudo timeout handling and integration with SudoKeepAlive.

    Args:
        message: Initial spinner message
        sudo_keepalive: Optional SudoKeepAlive instance to monitor
        monitor_sudo: Whether to monitor sudo status (default: False)
        check_sudo_fallback: Whether to fallback to sudo checking if keepalive fails
        on_sudo_expired: Callback function when sudo expires (optional)
    """

    def __init__(
        self,
        message: str,
        sudo_keepalive=None,
        monitor_sudo: bool = False,
        check_sudo_fallback: bool = True,
        on_sudo_expired: Optional[Callable] = None
    ):
        self.message = message
        self.sudo_keepalive = sudo_keepalive
        self.monitor_sudo = monitor_sudo or (sudo_keepalive is not None)
        self.check_sudo_fallback = check_sudo_fallback
        self.on_sudo_expired = on_sudo_expired

        self.spinner_style = "arc"
        self.spinner = RichSpinner(
            self.spinner_style, text=self._styled_text(message), style=TEXT_STYLE
        )
        self.live = RichLive(self.spinner, refresh_per_second=10)

        self._stop_event = threading.Event()
        self._sudo_checker_thread = None
        self._sudo_expired = False

    def _styled_text(self, text: str) -> RichText:
        return RichText(text, style=TEXT_STYLE)

    def _check_sudo_status(self):
        """Background thread to monitor sudo status as fallback"""
        check_interval = 60  # Check every minute

        while not self._stop_event.is_set():
            time.sleep(check_interval)

            # If we have a keepalive, check if it's still running
            if self.sudo_keepalive and self.sudo_keepalive.is_running:
                continue

            # Fallback: check sudo status directly
            try:
                result = subprocess.run(
                    ['sudo', '-n', 'true'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode != 0 and not self._sudo_expired:
                    self._sudo_expired = True
                    self._handle_sudo_expired()

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                if not self._sudo_expired:
                    self._sudo_expired = True
                    self._handle_sudo_expired()
            except:
                pass

    def _handle_sudo_expired(self):
        """Handle sudo expiration"""
        if self.on_sudo_expired:
            self.on_sudo_expired()
            return

        # Default handler
        self.live.stop()
        console = Console()
        console.print(
            RichText("\nSudo authorization expired!", style=WARNING_STYLE))
        console.print(
            RichText("Please enter your password when prompted:", style=TEXT_STYLE))

        try:
            subprocess.run(['sudo', '-v'], check=True, timeout=30)
            self._sudo_expired = False
            console.print(
                RichText("Sudo re-authenticated successfully!", style=SUCCES_STYLE))
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            console.print(
                RichText("Failed to re-authenticate sudo", style=ERROR_STYLE))
        finally:
            self.live.start()

    def _start_sudo_monitor(self):
        """Start sudo monitoring if enabled"""
        if self.monitor_sudo and not self._sudo_checker_thread:
            self._stop_event.clear()
            self._sudo_checker_thread = threading.Thread(
                target=self._check_sudo_status, daemon=True
            )
            self._sudo_checker_thread.start()

    def _stop_sudo_monitor(self):
        """Stop sudo monitoring"""
        self._stop_event.set()
        if self._sudo_checker_thread:
            self._sudo_checker_thread.join(timeout=1)
            self._sudo_checker_thread = None

    def update_text(self, new_message: str, log: bool = False) -> None:
        """Update the spinner text"""
        if log:
            logger.info(new_message)
        self.spinner.update(text=self._styled_text(new_message))

    def success(self, message: str, log: bool = False) -> None:
        """Show success message and stop spinner"""
        if log:
            logger.info(message)
        self.live.update(RichText(DONE_ICON + " " +
                         message, style=SUCCES_STYLE))

    def error(self, message: str, log: bool = False) -> None:
        """Show error message and stop spinner"""
        if log:
            logger.error(message)
        self.live.update(RichText(ERROR_ICON + " " +
                         message, style=ERROR_STYLE))

    def warning(self, message: str, log: bool = False) -> None:
        """Show warning message and stop spinner"""
        if log:
            logger.warning(message)
        self.live.update(RichText(WARNING_ICON + " " +
                         message, style=WARNING_STYLE))

    def __enter__(self):
        self.live.start()
        if self.monitor_sudo:
            self._start_sudo_monitor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.monitor_sudo:
            self._stop_sudo_monitor()
        self.live.stop()


# Functions for printing messages with styles
def print_sbdots_title() -> None:
    console = Console()
    text = figlet_format("SBDots")
    styled_text = RichText(text, style=HEADING_STYLE)
    console.print(styled_text)


def print_subtext(text: str) -> None:
    console = Console()
    console.print(RichText(text, style=SUBTEXT_STYLE))


def print_header(text: str) -> None:
    console = Console()
    console.print(text, style=HEADING_STYLE)


def print_info(text: str) -> None:
    console = Console()
    console.print(INFO_ICON + " " + text, style=TEXT_STYLE)


def print_success(text: str) -> None:
    console = Console()
    console.print(DONE_ICON + " " + text, style=SUCCES_STYLE)


def print_error(text: str) -> None:
    console = Console()
    console.print(ERROR_ICON + " " + text, style=ERROR_STYLE)


def print_warning(text: str) -> None:
    console = Console()
    console.print(WARNING_ICON + " " + text, style=WARNING_STYLE)


def chose(message: str, options: List[str]) -> str:
    """Display a message and present a list of options for the user to choose any one from."""
    console = Console()
    console.print(RichText(message, style=HEADING_STYLE))

    for i, option in enumerate(options, start=1):
        console.print(f"{i}. {option}", style=TEXT_STYLE)

    choices = [str(i) for i in range(1, len(options) + 1)]
    selected = Prompt.ask("Choose an option (number)", choices=choices)
    return options[int(selected) - 1]


def checklist(items: List[str], title: str = "List") -> List[str]:
    """Display a checklist and allow the user to select multiple items."""
    console = Console()
    console.print(title, style=HEADING_STYLE)

    for i, item in enumerate(items, start=1):
        console.print(f"{i}. {item}", style=TEXT_STYLE)

    selected_numbers = Prompt.ask(
        "Select items by their numbers separated by spaces (or 0 to skip)",
        default="0"
    )
    if selected_numbers.strip() == "0":
        return []

    selected_items = []
    for part in selected_numbers.split():
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(items):
                selected_items.append(items[idx])
    return selected_items


def confirm(title: str) -> bool:
    """Display a yes/no prompt."""
    console = Console()
    console.print(RichText(title, style=HEADING_STYLE))
    choice = Prompt.ask(choices=["y", "n"], default="y")
    return choice.lower() == "y"
