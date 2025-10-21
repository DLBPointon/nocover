import logging

from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Static, Button

logger = logging.getLogger(__name__)


class ErrorModal(ModalScreen):
    """
    Generic Error Modal which prints red error message
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

        logger.error(self.message)

    def compose(self):
        with Vertical(classes="error-box"):
            yield Static("Error!", classes="error")
            yield Static(f"\n\n{self.message}", markup=True)
            yield Button("OK", id="ok", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss()
