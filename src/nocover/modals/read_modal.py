from textual.screen import ModalScreen
from textual.widgets import Static, Button, Label
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult


class ReadModal(ModalScreen):
    """A popup screen with help / instructions."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Read Screen"

    def compose(self) -> ComposeResult:
        with Vertical(id="popup"):
            yield Label(f"Pinging the API that you've read the book...", id="popup-title")

            with Horizontal(id="popup-buttons"):
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.app.pop_screen()
        if event.button.id == "save":
            # ping API with read status
            self.app.pop_screen()
