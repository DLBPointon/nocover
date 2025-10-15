import os
import json

from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button, Checkbox
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from nocover.modals.add_modal import AddModal
from nocover.modals.error_page import ErrorModal

from nocover.hardcover.raw_queries import SEARCH_LISTS

from nocover.config import Config


class ListAddModal(AddModal):

    def parse_data(self):
        raw_data = self.get_query_from_api(SEARCH_LISTS)
        if isinstance(raw_data, bool):
            self.app.push_screen(
                ErrorModal("NO DATA!")
            )

        return raw_data


    def split_data(self, data):
        list_data: dict = {
            "slug": data["slug"],
            "name": data["name"],
            "followers_count": str(data["followers_count"]),
            "description": data["description"],
            "created_at": data["created_at"],
            "books_count": str(data["books_count"])
        }

        return list_data, data["list_books"]


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            list_data = self.parse_data()
            data = list_data["lists"][0]

            list, books = self.split_data(data)

            reformatted_books = self.get_book_list(books, "list")

            #the-esquire-75-best-sci-fi-books-of-all-time

            # now generate list_brl
            # now update list.csv

            self.dismiss("saved")

        elif event.button.id == "cancel":
            self.app.pop_screen()

        else:
            self.app.push_screen(
                ErrorModal("You shouldn't be here...")
            )


    def compose(self) -> ComposeResult:
        with Vertical(id="popup"):
            yield Label(f"So, you want to add a {self.title.title()}...", id="popup-title")
            yield self.slug_input

            with Horizontal(id="popup-buttons"):
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="primary")
