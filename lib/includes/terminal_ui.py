from rich.text import Text as RichText
from rich.live import Live as RichLive
from rich.spinner import Spinner as RichSpinner
from rich.style import Style as RichStyle
from rich.console import Console

from functools import partial
from pyfiglet import figlet_format
from typing import List

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
    """
    Context manager for showing a live console spinner using `rich`.

    Allows updating the spinner text in real time and replacing it with
    styled success, error, or warning messages when done.
    
    args:
        message (str): The initial message to display with the spinner.
        
    methods:
        update_text(new_message: str): Update the spinner text.
        success(message: str): Display a success message and stop the spinner.
        error(message: str): Display an error message and stop the spinner.
        warning(message: str): Display a warning message and stop the spinner.
        
    usage:
        >>> with Spinner("Processing data...") as spin:
        ...     time.sleep(2)
        ...     spin.update_text("Still working...")
        ...     time.sleep(1)
        ...     spin.success("Done!")
    """
    def __init__(self, message: str):
        self.message = message
        self.spinner_style = "arc"
        self.spinner = RichSpinner(self.spinner_style, text=self._styled_text(message), style=TEXT_STYLE)
        self.live = RichLive(self.spinner, refresh_per_second=10)

    def _styled_text(self, text: str) -> RichText:
        return RichText(text, style=TEXT_STYLE)

    def _update_renderable(self, renderable: str) -> None:
        self.live.update(renderable)
        
    def update_text(self, new_message: str) -> None:
        self.spinner.text = self._styled_text(new_message)
    
    def success(self, message: str) -> None:
        self._update_renderable(RichText(DONE_ICON + " " + message, style=SUCCES_STYLE))

    def error(self, message: str) -> None:
        self._update_renderable(RichText(ERROR_ICON + " " + message, style=ERROR_STYLE))
    
    def warning(self, message: str) -> None:
        self._update_renderable(RichText(WARNING_ICON + " " + message, style=WARNING_STYLE))
    
    def __enter__(self):
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.live.stop()
    
# Functions for printing messages with styles
def print_hyprdots_title() -> None:
    console = Console()
    text = figlet_format("HyprDots")
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
    """
    Display a message and present a list of options for the user to choose any one from.

    Args:
        message (str): the message to display
        options (List[str]): the options to choose from

    Returns:
        str: the chosen option
    """
    console = Console()
    console.print(RichText(message, style=HEADING_STYLE))
    
    for i, option in enumerate(options, start=1):
        console.print(f"{i}. {option}", style=TEXT_STYLE)
    
    while True:
        choice = input("Choose an option (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            console.print(RichText("Invalid choice. Please try again.", style=ERROR_STYLE))
            
            
def checklist(items: List[str], title: str = "List") -> List[str]:
    """ 
    Display a checklist and allow the user to select multiple items.
    
    Args:
        items (List[str]): the items to display in the checklist
        title (str): the title of the checklist
    
    Returns:
        List[str]: the selected items
    """
    console = Console()
    console.print(title, style=HEADING_STYLE)
    
    for i, item in enumerate(items, start=1):
        console.print(f"{i}. {item}", style=TEXT_STYLE)
    
    while True:
        chosen: str = input("Select items by their numbers separated by empty spaces(eg: 1 2 3), type 0 to skip: ")
        selected_items = []

        if chosen.strip() == "0":
            return []
        
        for part in chosen.split():
            if part.isdigit():
                index = int(part) - 1
                if 0 <= index < len(items):
                    selected_items.append(items[index])
                else:
                    console.print(RichText(f"Invalid choice: {part}. Please try again.", style=ERROR_STYLE))
                    continue
                                
        if selected_items:
            return selected_items