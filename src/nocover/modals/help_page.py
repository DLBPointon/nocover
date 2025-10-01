from textual.screen import ModalScreen
from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal

class HelpModal(ModalScreen):
    """A popup screen with help / instructions."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Help Screen"

    def compose(self):
        with Vertical(id="popup"):
            yield Static("[b]Help & Shortcuts[/b]", id="popup-title")

            yield Static(
                "\n[b]Books Tab[/b]:\n"
                "This tab group is populated by the Hardcover API,\n"
                "meaning that only books in Account bound lists will appear here\n\n"
                "[b]Series Tab[/b]:\n"
                "This Tab is populated by you, eventually you will be able to 'quick add'\n"
                "a series, and get data for that series appear in the Details Panel. \n"
                "adding a series will automatically generate a BRL (book-reading-list).\n\n"
                "[b]General[/b]:\n"
                "- q: Quit the app\n"
                "- h: Show this help modal\n",
                id="popup-buttons"
            )

            with Horizontal(id="help-buttons"):
                yield Button("Close", id="close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.app.pop_screen()
