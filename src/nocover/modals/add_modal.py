import requests
from pathlib import Path

from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from nocover.modals.error_page import ErrorModal

from nocover.config import Config

from nocover.brl.book import Book
from nocover.brl.list_book import ListBook


class AddModal(ModalScreen):
    def __init__(self, title: str, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title: str         = title
        self.db_url: str        = config.db_url
        self.config_token: str  = config.token
        self.config: str = config
        self.slug_input: Input  = Input(
            placeholder="Item to add locally (Use the slug!): space-marine-battles",
            type="text",
            classes="popup-text"
        )

        self.save_location: Input = Input(
            placeholder=config.default_folders[title],
            type="text",
            classes="popup-text"
        )


    def compose(self) -> ComposeResult:
        with Vertical(id="popup"):
            yield Label(f"So, you want to add a {self.title.title()}...", id="popup-title")
            yield self.slug_input

            yield Label("Save to folder (optional):")
            yield self.save_location

            with Horizontal(id="popup-buttons"):
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="primary")


    def validate_save_directory(self):
        try:
            Path(self.save_location).mkdir(parents=True, exist_ok=True)
            return self.save_location
        except:
            ErrorModal(f"Can't make directory for: {self.save_location}")
            # Might need to be something here

    def split_data(self, data, search_attribute):
        list_data: dict = {
            "slug": data.get("slug", self.slug_input.value),
            "name": data.get("name", data["question"]),
            "followers_count": str(data.get("followers_count", "NA")),
            "description": data["description"],
            "created_at": data["created_at"],
            "books_count": str(data["books_count"])
        }

        return list_data, data[search_attribute]


    def parse_data(self, query: str):
        raw_data = self.get_query_from_api(query)
        if isinstance(raw_data, bool):
            self.app.push_screen(
                ErrorModal("NO DATA!")
            )

        return raw_data


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


    def update_index_file(self, item_name, item_count, brl_file):
        new_item = f"{item_name}\t{item_count}\t{brl_file}"

        with open(self.config.index_file_dict[self.title], "r") as file_list:
            for line in file_list:
                if line == new_item:
                    self.app.push_screen(
                        ErrorModal(f"{self.title.title()} already in Series List!")
                    )

        with open(self.config.index_file_dict[self.title], "a") as file_list:
            file_list.write(new_item)
