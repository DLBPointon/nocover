
from textual.widgets import Label, Button
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from nocover.modals.add_modal import AddModal
from nocover.modals.error_page import ErrorModal

from nocover.hardcover.raw_queries import SEARCH_LISTS

from nocover.brl.generate_brl import generate_brl_file


class ListAddModal(AddModal):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            list_data = self.parse_data(SEARCH_LISTS)
            data = list_data["lists"][0]

            list_info, books = self.split_data(data, "list_data")

            reformatted_books = self.get_book_list(books, "list")

            save_location = self.validate_save_directory()

            generate_brl_file(
                book_list = reformatted_books,
                save_location = f"{save_location}/{list_info["slug"]}.brl",
                series_data = list_info,
                add_tags = False,
                universe = "",
                universe_position = ""
            )

            self.update_index_file(
                list_info["name"],
                len(reformatted_books),
                f"{save_location}\n"
            )

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
