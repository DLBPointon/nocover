import os
import requests

from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button, Checkbox
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from nocover.hardcover.raw_queries import SEARCH_SERIES

from nocover.modals.add_modal import AddModal
from nocover.modals.error_page import ErrorModal

from nocover.config import Config

from nocover.brl.book import Book
from nocover.brl.generate_brl import generate_brl_file

class SeriesAddModal(AddModal):
    def __init__(self, title: str, config: Config, *args, **kwargs):
        super().__init__(title, config, *args, **kwargs)

        self.universe: Input        = Input(
            placeholder="Universe of series (optional): Warhammer",
            type="text",
            classes="popup-text"
        )
        self.universe_position: Input = Input(
            placeholder = "Number position of series in Universe",
            type="text",
            classes="popup-text"
        )


    def compose(self) -> ComposeResult:
        with Vertical(id="popup"):
            yield Label(f"So, you want to add a {self.title.title()}...", id="popup-title")
            yield self.slug_input
            yield self.universe
            yield self.universe_position

            with Horizontal(id="popup-checkboxes"):
                yield Checkbox("Include Tags", id="opt_tags", value=True)
                yield Checkbox("Include Ghost Volumes", id="opt_ghosts", value=False)
                yield Checkbox("Include Compilations", id="opt_compilations", value=False)

            with Horizontal(id="popup-buttons"):
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="primary")


    def validate_series(self, slug):
        """
        Variant of the function found in the general_functions.py file
        """
        new_query: str = SEARCH_SERIES.replace("SLUG", f'"{self.slug_input.value}"')

        reqHeaders: dict[str, str] = {
            'Authorization': 'Bearer ' + self.config_token
        }

        response = requests.post(
            url     = self.db_url,
            headers = reqHeaders,
            json    = {"query": new_query}
        )

        if response.status_code == 200:
            content = response.json()["data"]
            return content["series"][0], content["book_series"]
        else:
            return False, False


    def reformat_series_data(self, data):
        return {
            "name" :                data["name"],
            "author_name" :         data["author"]["name"],
            "author_personal" :     data["author"]["name_personal"],
            "series_slug" :         self.slug_input.value,
            "series_universe" :     "NA" if self.universe.value is None else self.universe.value,
            "series_universe_pos":  "NA" if self.universe_position.value is None else self.universe_position.value,
            "series_description" :  data["description"],
            "series_creator" :      data["creator"],
            "series_completed" :    data["is_completed"],
            "slug_match" :          (True if data["slug"] == self.universe.value else False),
            "series_book_count" :   data["books_count"]
        }


    def remove_ghosts(self, data):
        """
        Database currently has alot of books which are assigned the same
        position, such as books that are actually editions,
        this function removes this by removing those which have no
        default edition. E.g. a Ghost
        """
        book_list = []
        ghosts = []
        for i in data:
            if i["book"]["default_cover_edition"] is None:
                ghosts.append(i["book"]["slug"])
            else:
                book_list.append(i)

        return book_list, ghosts


    def remove_editions(self, data):
        """
        Shrink the list by keeping only the canonical slug book.
        """
        book_list = []

        for i in data:
            default_slug = i["book"]["default_cover_edition"]["book"]["slug"]
            if i["book"]["slug"] == default_slug:
                book_list.append(i)

        return book_list


    def remove_compilations(self, data):
        """
        Find books which are compilations of books inside the series
        user may or may not want these included in output
        """
        book_list = []
        yes_compilations = []

        for i in data:
            comp = i["book"]["default_cover_edition"]["book"]["compilation"]
            if comp in [False, None]:
                book_list.append(i)
            else:
                yes_compilations.append(i["book"]["slug"])

        return book_list, yes_compilations


    def clean_book_data(self, data):
        """
        Cleans the book lists by
        removing ghosts
        removing editions

        by user choice also remove compilations
        """

        add_comp = self.query_one("#opt_compilations", Checkbox).value
        add_ghosts = self.query_one("#opt_ghosts", Checkbox).value

        if not add_ghosts:
            no_ghosts, yes_ghosts = self.remove_ghosts(data)
            out_data = self.remove_editions(no_ghosts)

        yes_compilations = []
        if not add_comp:
            out_data, yes_compilations = self.remove_compilations(out_data)

        return out_data, yes_ghosts, yes_compilations


    def reformat_book_data(self, data):
        clean_book_list, ghosts, compilations = self.clean_book_data(data)
        book_list = self.get_book_list(clean_book_list)
        return {
            "raw_book_count" :      len(data),
            "clean_book_count" :    len(book_list),
            "series_ghosts" :       ghosts,
            "series_compilations" : compilations,
            "book_data" :           sorted(
                                        book_list,
                                        key=lambda x: x.series_position,
                                        reverse=False
                                    )
        }


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            series_data, book_data = self.validate_series(self.slug_input.value)

            if isinstance(series_data, bool) and isinstance(book_data, bool):
                self.app.push_screen(
                    ErrorModal("Invalid series slug - no data returned from Hardcover")
                )

            item_path = self.make_sure_item_dir_exists()

            brl_location: str = item_path + self.slug_input.value + ".brl"
            if not os.path.exists(brl_location):
                reformatted_series_data: dict[str, str] = self.reformat_series_data(series_data)

                reformatted_book_data: dict[str, str] = self.reformat_book_data(book_data)

                if len(reformatted_book_data["book_data"]) == 0:
                    self.app.push_screen(
                        ErrorModal(f"{reformatted_series_data["name"]} has 0 books!")
                    )

                # Generate a book-reading-list file for series
                generate_brl_file(
                    book_list = reformatted_book_data["book_data"],
                    save_location = brl_location,
                    series_data = reformatted_series_data,
                    add_tags = self.query_one("#opt_tags", Checkbox).value,
                    universe = self.universe.value,
                    universe_position = self.universe_position.value
                )

                # Output these too?
                # "series_ghosts" : ghosts,
                # "series_compilations" : compilations,

                # add data["name"], slug, path_to_brl to an index file
                self.update_index_file(
                    reformatted_series_data["name"],
                    reformatted_book_data["clean_book_count"],
                    item_path + reformatted_series_data["series_slug"] + ".brl\n"
                )

                self.dismiss("saved")

            else:
                self.app.push_screen(
                    ErrorModal("Series already exists! (Rebuilding a series is on the TODO list)")
                )

        elif event.button.id == "cancel":
            self.app.pop_screen()
