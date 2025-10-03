import os

from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button, Checkbox
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from nocover.modals.add_modal import AddModal
from nocover.modals.error_page import ErrorModal

from nocover.config import Config


class ListAddModal(AddModal):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.app.push_screen(
                ErrorModal("save... yay")
            )
        elif event.button.id == "cancel":
            self.app.pop_screen()
        else:
            self.app.push_screen(
                ErrorModal("You shouldn't be here...")
            )
