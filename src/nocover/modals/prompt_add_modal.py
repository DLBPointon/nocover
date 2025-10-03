import os
import json
import requests

from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button, Checkbox
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from nocover.modals.add_modal import AddModal
from nocover.modals.error_page import ErrorModal

from nocover.hardcover.raw_queries import FOLLOWED_PROMPTS

from nocover.config import Config


class PromptAddModal(AddModal):

    def sort_api_return(self):
        """Get data from API and parse into header + book list"""

        api_data = self.get_query_from_api(FOLLOWED_PROMPTS)
        if isinstance(api_data, bool):
           if not api_data:
              ErrorModal(
                  message = "Error in return from API - check your API key and internet connection"
              )
        elif isinstance(api_data, dict):
            #header, book_list = self.clean_data(api_data)
            with open("testing.json", "w") as out:
                #json.dump(api_data["me"][0]["followed_prompts"],out)

        else:
            ErrorModal(
                message = "You shouldn't be here..."
            )



    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.sort_api_return()
        elif event.button.id == "cancel":
            self.app.pop_screen()
        else:
            self.app.push_screen(
                ErrorModal("You shouldn't be here...")
            )
