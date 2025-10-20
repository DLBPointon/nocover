
from textual.widgets import Button

from nocover.modals.add_modal import AddModal
from nocover.modals.error_page import ErrorModal

from nocover.hardcover.raw_queries import SEARCH_PROMPT

from nocover.brl.generate_brl import generate_brl_file


class PromptAddModal(AddModal):


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            prompt_data = self.parse_data(SEARCH_PROMPT)

            data = prompt_data["prompts"][0]

            prompt_info, books = self.split_data(data, "prompt_books")

            reformatted_books = self.get_book_list(books, "prompts")

            save_location = self.validate_save_directory()

            generate_brl_file(
                book_list = reformatted_books,
                save_location = f"{save_location}/{self.slug_input.value}.brl",
                series_data = prompt_info,
                add_tags = False,
                universe = "",
                universe_position = ""
            )

            self.update_index_file(
                prompt_info["name"],
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
