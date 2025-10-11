from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

class LoadingScreen(Container):
    """
    Full-screen overlay with text-only loading status.
    """

    # Generated on https://patorjk.com/software/taag/
    ASCII_LOGO = r"""
    _   _       _____
   | \ | |     /  __ \
   |  \| | ___ | /  \/ _____   _____ _ __
   | . ` |/ _ \| |    / _ \ \ / / _ \ '__|
   | |\  | (_) | \__/\ (_) \ V /  __/ |
   \_| \_/\___/ \____/\___/ \_/ \___|_|

    """

    def compose(self) -> ComposeResult:
        yield Static(self.ASCII_LOGO, id="ascii_logo")
        yield Static("Preparing data...", id="status_text")

    def update_status(self, message: str):
        """Update the message text dynamically."""
        status = self.query_one("#status_text", Static)
        status.update(message)
