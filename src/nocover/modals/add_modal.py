import os
import requests

from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button, Checkbox
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from nocover.modals.error_page import ErrorModal

from nocover.config import Config

from nocover.brl.book import Book
from nocover.brl.list_book import ListBook
from nocover.brl.generate_brl import generate_brl_file


class AddModal(ModalScreen):
    def __init__(self, title: str, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title: str         = title
        self.db_url: str        = config.db_url
        self.config_token: str  = config.token
        self.config_folder: str = config.path
        self.slug_input: Input  = Input(
            placeholder="Item to add locally (Use the slug!): space-marine-battles",
            type="text",
            classes="popup-text"
        )


    def compose(self) -> ComposeResult:
        with Vertical(id="popup"):
            yield Label(f"So, you want to add a {self.title.title()}...", id="popup-title")
            yield self.slug_input

            with Horizontal(id="popup-buttons"):
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="primary")


    def get_query_from_api(self, query) -> dict[str, any] | bool: # ty: ignore[invalid-type-form]
        """
        Get data from api with given query
        """
        new_query: str = query.replace("SLUG", f'"{self.slug_input.value}"')

        reqHeaders: dict[str, str] = {
            'Authorization': self.config_token
        }

        response = requests.post(
            url     = self.db_url,
            headers = reqHeaders,
            json    = {"query": new_query}
        )

        if response.status_code == 200:
            return response.json()["data"]
        else:
            return False


    def sort_books(self, book_list):
        return sorted(
                    book_list,
                    key=lambda x: x.series_position,
                    reverse=False
                )


    def get_book_list(self, book_list: list[dict], type: str) -> list[Book|ListBook]:
        """Convert dict of books into list of book objects"""
        if type == "list":
            return self.sort_books([ ListBook(book_dict=book) for book in book_list ])
        else:
            return self.sort_books([ Book(book_dict=book) for book in book_list ])

    def make_sure_item_dir_exists(self):
        """Make sure that the item dir exists and return its path"""
        series_path: str = self.config_folder + f"/{self.title}_data/"
        if not os.path.exists(series_path):
            os.mkdir(series_path)
        return series_path


    def update_index_file(self, item_name, item_count, brl_file):
        new_item = f"{item_name},{item_count},{brl_file}"

        with open(self.config_folder + f"/{self.title}_list.csv", "r") as file_list:
            for line in file_list:
                if line == new_item:
                    self.app.push_screen(
                        ErrorModal(f"{self.title.title()} already in Series List!")
                    )

        with open(self.config_folder + "/{self.title}_list.csv", "a") as file_list:
            file_list.write(new_item)
