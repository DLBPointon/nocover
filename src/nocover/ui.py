# General Package Imports
import os
from typing import final

# Textual Package Import
from textual.app import App, ComposeResult
from textual.screen import ModalScreen, Screen
from textual.binding import Binding
from textual.containers import (
    Horizontal,
    Vertical,
    HorizontalScroll,
    VerticalScroll,
    Container,
)
from textual.widgets import Label, TabbedContent, TabPane, ListView
from textual.widgets import Footer, Button, Input, Static, Link

# Local App Importsfrom textual.widgets import Label
from nocover.config import Config
from nocover.list_items import (
    BookListItem,
    SeriesListItem,
    ListListItem,
    PromptListItem,
    ProfilePublicListItem,
    ProfileBooksListItem,
    ProfilePersonalListItem,
)
from nocover.loading_screen import LoadingScreen
from nocover.general_functions import json_dump, max_key_len

# Local App Modal Imports
from nocover.general_classes import NCHeader
from nocover.modals.help_page import HelpModal
from nocover.modals.error_page import ErrorModal
from nocover.modals.series_add_modal import SeriesAddModal
from nocover.modals.list_add_modal import ListAddModal
from nocover.modals.prompt_add_modal import PromptAddModal
from nocover.modals.read_modal import ReadModal

# Local App Hardcover Imports
from nocover.hardcover.raw_queries import (
    HARDCOVER_PROFILE_QUERY,
    HARDCOVER_USER_BOOKS_BY_STATUS,
    FOLLOWED_LISTS,
    FOLLOWED_PROMPTS,
)
from nocover.hardcover.get_profile import Profile
from nocover.hardcover.get_books import BookData as UserBookData
from nocover.hardcover.get_lists import ListData as UserListData
from nocover.hardcover.get_prompts import PromptData as UserPromptData
from nocover.brl.read_series_brl import SeriesBrlData

DEFAULT_BOOK_COVER = """
+-------------+
|   📘 ???    |
|             |
|   No Img    |
| Support Yet |
+-------------+
"""


class MissingConfigOption(ModalScreen[None]):
    """ """

    def __init__(self, config_path: str, config_data: Config) -> None:
        super().__init__()
        self.config_path: str = config_path
        self.config_data: Config = config_data
        self.config_input: Input = Input(placeholder="Hardcover Token")
        self.email_input: Input = Input(placeholder="eto_demerzel@trantor.empire")

    def compose(self) -> ComposeResult:
        with Vertical(classes="popup"):
            yield Label("Config file missing. Please enter your Hardcover API Token:")
            yield self.config_input

            yield Label("It's helpful to have your email too!")
            yield self.email_input

            with Horizontal():
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            # validated_input = self.validate_config_input()

            with open(self.config_path + "/.config", "w") as f:
                data: dict[str, str] = {
                    "HARDCOVER_API_TOKEN": self.config_input.value,
                    "EMAIL": self.email_input.value,
                }
                json_dump(data, f)

            self.app.pop_screen()
            self.app.push_screen(
                NCScreen(Config(self.config_path))
            )  # go to main screen

        elif event.button.id == "cancel":
            self.app.exit("User cancelled config setup.")


class DetailsPanel(Static):
    """
    The Right Side Panel for DetailsPanel, will show either of:
        - Books info
        - Series info
        - Personal profile info
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "Details Panel"

    def compose(self) -> ComposeResult:
        with Horizontal(id="BookBox"):
            # Left containter is the ASCII cover (static)
            # yield Static(
            #     content=DEFAULT_BOOK_COVER, id="book_cover", markup=False
            # )

            # Right container is the details container we can fill dynamically
            # Here it has a static placeholder which i think looks cool af
            # generated at:
            # https://patorjk.com/software/taag/#p=display&f=Alligator2&t=NC&x=none&v=4&h=4&w=80&we=false
            yield VerticalScroll(
                Static(
                    content="""
                    ::::    :::  ::::::::
                    :+:+:   :+: :+:    :+:
                    :+:+:+  +:+ +:+
                    +#+ +:+ +#+ +#+
                    +#+  +#+#+# +#+
                    #+#   #+#+# #+#    #+#
                    ###    ####  ########
                    """
                ),
                id="details_rows",
            )

    def update_series_details(self, data: SeriesBrlData) -> None:
        """Update panel with ListItem per book in SeriesBrlData."""
        container = self.query_one("#details_rows", VerticalScroll)
        container.remove_children()

        # --- Series Card ---
        series_block = Vertical(classes="detail-series")

        series_block.border_title = f"Series overview: [b][u]{data.series_name}[/u][/b]"

        container.mount(series_block)

        series_block.mount(Horizontal(*[Label(data.universe)], classes="detail-row"))

        series_block.mount(
            Horizontal(
                *[
                    Label("Database: ", classes="detail-key"),
                    Link(
                        str(
                            f"{data.database_info['@Name']}/{data.database_info['@Item']}"
                        ),
                        url=f"https://hardcover.app/series/{data.database_info['@Item']}",
                        tooltip=f"Head to Hardcover page for {data.series_name}",
                    ),
                ],
                classes="detail-row",
            )
        )

        series_block.mount(
            Horizontal(
                *[
                    Label("Description: ", classes="detail-key"),
                    Label(data.series_description, classes="detail-value"),
                ],
                classes="detail-row",
            )
        )

        # --- Book Cards ---
        books = data.series_data["Books"]["Book"]
        if isinstance(books, dict):  # handle single-book edge case
            books = [books]

        for idx, book in enumerate(books, start=1):
            # Mount the book_block container with key information as title
            book_block = Vertical(classes="detail-book")
            book_name = book.get("@Name", "Unknown")
            book_position = book.get("@Position", "Unknown")
            book_block.border_title = (
                f"Book {idx} -:- {book_name} -:- Position: {book_position}"
            )
            container.mount(book_block)

            # Add rows into the book_block
            max_key: int = max_key_len(book.keys())

            for key, value in book.items():
                if key == "Tag":
                    value = "\n".join(value)

                # Skip these from the outputs
                if key not in ["@Name", "@Position"]:
                    new_key = key.replace("@", "")

                    row = Horizontal(
                        Label(
                            f"{new_key}: ".ljust(max_key + 2).title(),
                            classes="detail-key",
                        ),
                        (
                            Label(value, classes="detail-value")
                            if new_key != "Database"
                            else Link(
                                f"{value['@Name']}/{value['@Item']}",
                                url=f"https://hardcover.app/books/{value['@Item']}",
                                tooltip=f"Head to Hardcover page for {book_name}",
                            )
                        ),
                        classes="detail-row",
                    )
                    book_block.mount(row)

    def update_list_details(
        self, list_data, book_data
    ) -> None:
        container = self.query_one("#details_rows", VerticalScroll)
        container.remove_children()

        # --- Series Card ---
        max_key: int = max_key_len(list_data.keys())

        series_block = Vertical(classes="detail-series")

        series_block.border_title = f"List overview: [b][u]{list_data['name']}[/u][/b]"

        container.mount(series_block)

        series_block.mount(
            Horizontal(
                *[
                    Label(
                        "Database: ".ljust(max_key + 2).title(), classes="detail-key"
                    ),
                    Link(
                        str(f"harcover/{list_data['slug']}"),
                        url=f"https://hardcover.app/list/{list_data['slug']}",
                        tooltip=f"Head to Hardcover page for {list_data['name']}",
                    ),
                ],
                classes="detail-row",
            )
        )

        series_block.mount(
            Horizontal(
                *[
                    Label(
                        "Length of List: ".ljust(max_key + 2).title(),
                        classes="detail-key",
                    ),
                    Label(str(list_data["book_count"]), classes="detail-value"),
                ],
                classes="detail-row",
            )
        )

        series_block.mount(
            Horizontal(
                *[
                    Label(
                        "Description: ".ljust(max_key + 2).title(), classes="detail-key"
                    ),
                    Label(list_data["description"], classes="detail-value"),
                ],
                classes="detail-row",
            )
        )

        series_block.mount(
            Horizontal(
                *[
                    Label(
                        "Follower Count: ".ljust(max_key + 2).title(),
                        classes="detail-key",
                    ),
                    Label(str(list_data["follower_count"]), classes="detail-value"),
                ],
                classes="detail-row",
            )
        )

        series_block.mount(
            Horizontal(
                *[
                    Label(
                        "Like Count: ".ljust(max_key + 2).title(), classes="detail-key"
                    ),
                    Label(str(list_data["like_count"]), classes="detail-value"),
                ],
                classes="detail-row",
            )
        )

        for idx, book in enumerate(book_data, start=1):
            # Mount the book_block container with key information as title
            book_block = Vertical(classes="detail-book")
            book_name = book["book_title"]
            book_position = (
                "NA" if book["list_position"] is None else book["list_position"]
            )
            book_block.border_title = (
                f"Book {idx} -:- {book_name} -:- Position: {book_position}"
            )
            container.mount(book_block)

            for key, value in book.items():
                max_key: int = max_key_len(book.keys()) + 2

                key = " ".join(key.split("_"))
                key = key.ljust(max_key).title()
                value = "\n".join(value) if key == "book_tags" else str(value)
                row = Horizontal(
                    Label(f"{key}: ".title(), classes="detail-key"),
                    Label(value, classes="detail-value"),
                    classes="detail-row",
                )
                book_block.mount(row)

            # Add rows into the book_block
            # for key, value in book.items():

    def update_details(self, data: dict[str, str]):
        """
        Update panel with arbitrary key:value pairs from `data`.
        Returns a DataTable containing rows of key: value formatted
        somewhat nicely.
        """
        # ascii_text = data.pop("book_cover", DEFAULT_BOOK_COVER)
        # self.query_one("#book_cover", Static).update(ascii_text)

        container = self.query_one("#details_rows", VerticalScroll)
        container.remove_children()

        if not data:
            return

        max_key: int = max_key_len(data.keys())

        # get list of keys in dict, and re-order so description is last
        # ugly i know
        key_list = list(data.keys())
        for i in ["description", "slug"]:
            if i in key_list:
                key_list.remove(i)
                if i == "description":
                    key_list.append("description")

        for key in key_list:
            # for key, value in data.items():
            # create row and mount it into the container first
            row: Horizontal = Horizontal(classes="detail-row")
            container.mount(row)

            new_key = " ".join(key.split("_"))

            # now we can mount children into the row

            row.mount(
                Label(f"{new_key.ljust(max_key + 2).title()}", classes="detail-key")
            )

            # The join/split attempts to remove some of the double spacing
            # going on in the large text fields
            if key == "book_series":
                info = [i["series"]["name"] for i in data[key] if i["series"]]
                info = "None" if len(info) < 1 else info
            else:
                info = data[key]

            if key == "title":
                row.mount(
                    Link(
                        str(info),
                        url=f"https://hardcover.app/books/{data['slug']}",
                        tooltip=f"Head to Hardcover page for {info}",
                    )
                )

            else:
                row.mount(Label(content=str(info), classes="detail-value", markup=True))


class MainContainer(TabbedContent):
    def __init__(
        self,
        profile_data: Profile,
        book_data: UserBookData,
        config_data: Config,
        list_data: UserListData,
        prompt_data: UserPromptData,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.profile_data = profile_data
        self.book_data = book_data
        self.list_data = list_data
        self.prompt_data = prompt_data
        self.border_title = "Data Panel"
        self.config_data = config_data
        self.book_by_Status = book_data.dict_by_status

    @staticmethod
    def createPromptListItem(self):
        return [
            PromptListItem(line)
            for line in open(self.config_data.index_file_dict["prompts"])
        ]

    @staticmethod
    def createProfileListItem(profile_data):
        return [
            ProfilePublicListItem(profile_data),
            ProfileBooksListItem(profile_data),
            ProfilePersonalListItem(profile_data),
        ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="list_books", id="tab_panel"):
            with TabPane("Books", id="list_books"):
                with TabbedContent(initial="status-want-to-read"):
                    for status, titles in self.book_by_Status.items():
                        with TabPane(
                            title=status.title(), id=f"status-{status.lower()}"
                        ):
                            yield ListView(
                                *[
                                    BookListItem(book_data)
                                    for book_title, book_data in titles.items()
                                ]
                            )

            with TabPane(title="Series", id="list_series"):
                with Horizontal(id="button-bar"):
                    yield Button(
                        "Refresh", id="refresh_active", classes="general-button"
                    )
                    yield Button(
                        "Remove",
                        id="remove_series",
                        classes="general-button",
                        disabled=True,
                    )
                yield ListView(
                    *[
                        SeriesListItem(
                            series_name=line.split("\t")[0],
                            series_count=str(line.split("\t")[1]),
                            series_brl=line.split("\t")[2],
                        )
                        for line in open(self.config_data.index_file_dict["series"])
                    ],
                    id="series_list",
                )

            with TabPane(title="Lists", id="list_list"):
                with TabbedContent(initial="status-list-followed"):
                    with TabPane(title="Followed lists", id="status-list-followed"):
                        yield ListView(
                            *[
                                ListListItem(
                                    i,
                                    self.list_data.lists[i]["list_information"]["name"],
                                    self.list_data.lists[i],
                                )
                                for i in self.list_data.lists
                            ]
                        )

                    with TabPane(
                        title="Manually Followed", id="status-list-manual-followed"
                    ):
                        yield ListView(
                            *[
                                SeriesListItem(
                                    series_name=line.split("\t")[0],
                                    series_count=str(line.split("\t")[1]),
                                    series_brl=line.split("\t")[2],
                                )
                                for line in open(
                                    self.config_data.index_file_dict["lists"]
                                )
                            ],
                            id="series_list",
                        )

            with TabPane(title="Prompts", id="list_prompt"):
                with TabbedContent(initial="status-prompt-followed"):
                    with TabPane(title="Followed Prompts", id="status-prompt-followed"):
                        yield ListView(
                            *[
                                ListListItem(
                                    i,
                                    self.prompt_data.lists[i]["list_information"][
                                        "name"
                                    ],
                                    self.prompt_data.lists[i],
                                )
                                for i in self.prompt_data.lists
                            ]
                        )

                    with TabPane(title="Manual Follows", id="status-prompt-manual"):
                        yield ListView(
                            *[
                                SeriesListItem(
                                    series_name=line.split("\t")[0],
                                    series_count=str(line.split("\t")[1]),
                                    series_brl=line.split("\t")[2],
                                )
                                for line in open(
                                    self.config_data.index_file_dict["prompts"]
                                )
                            ],
                            id="series_list",
                        )

            with TabPane(title="Profile", id="profile_page"):
                yield ListView(
                    *self.createProfileListItem(self.profile_data),
                    id="list_view_profile",
                )

    def refresh_series_list(self):
        """Reload the series list from the TSV file."""

        # if active.pane == series
        series_list = self.query_one("#series_list", ListView)
        series_list.clear()

        with open(self.config_data.index_file_dict["series"]) as f:
            for line in f:
                if not line == "\n":
                    name, count, brl = line.strip().split("\t")

                    # Doesn't actually get triggered... annoyingly
                    if not os.path.exists(brl.strip()):
                        ErrorModal(f"BRL file does not exist for: {name}")

                    series_list.append(
                        SeriesListItem(
                            series_name=name, series_count=str(count), series_brl=brl
                        )
                    )

    def remove_series(self):
        series_list = self.query_one("#series_list", ListView)
        selected = series_list.index
        if selected is None:
            return  # nothing selected, button should be disabled anyway

        item = series_list.children[selected]

        series_name = item.series_name
        series_count = item.series_count
        series_brl = item.series_brl

        # Remove from UI
        item.remove()

        # Remove from CSV
        csv_file = self.config_data.index_file_dict["series"]
        with open(csv_file, "r") as f:
            lines = f.readlines()

        # make tmp file
        with open(f"{csv_file}.tmp", "w") as n:
            for line in lines:
                if not line == f"{series_name},{series_count},{series_brl}":
                    n.write(line)

        # remove original, cp tmp over it
        os.remove(csv_file)
        os.rename(f"{csv_file}.tmp", csv_file)
        os.remove(series_brl.strip())

        # Disable button again
        remove_button = self.query_one("#remove_series", Button)
        remove_button.disabled = True

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id == "series_list":
            remove_button = self.query_one("#remove_series", Button)
            # Enable only if something is selected
            remove_button.disabled = event.item is None

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "refresh_active":
            self.refresh_series_list()
        elif event.button.id == "add_series":
            self.app.push_screen(SeriesAddModal("series", self.config_data))
        elif event.button.id == "remove_series":
            self.remove_series()


class NCScreen(Screen):
    """Main screen with internal full-screen loading overlay."""

    CSS_PATH = "layout.tcss"

    def __init__(self, config_data):
        super().__init__()
        self.config_data = config_data
        self.profile_data = None
        self.book_data = None

    def compose(self) -> ComposeResult:
        yield Container(id="content")  # placeholder for main content
        yield LoadingScreen(id="loading_overlay")

    async def on_mount(self):
        """Start data preparation when screen mounts."""
        self.run_worker(self.prepare_data())

    async def prepare_data(self):
        """Load data in stages and update status."""
        overlay = self.query_one("#loading_overlay", LoadingScreen)
        offline = False

        overlay.update_status("Loading Profile data...")
        self.profile_data = Profile(
            query=HARDCOVER_PROFILE_QUERY,
            api_path="profile",
            config_path=self.config_data,
            offline=offline,
        )

        overlay.update_status("Loading Book data...")
        self.book_data = UserBookData(
            query=HARDCOVER_USER_BOOKS_BY_STATUS,
            api_path="user_books",
            config_path=self.config_data,
            offline=offline,
        )

        overlay.update_status("Loading saved List data...")
        self.list_data = UserListData(
            query=FOLLOWED_LISTS,
            api_path="lists",
            config_path=self.config_data,
            offline=offline,
        )

        overlay.update_status("Loading saved Prompt data...")
        self.prompt_data = UserPromptData(
            query=FOLLOWED_PROMPTS,
            api_path="prompts",
            config_path=self.config_data,
            offline=offline,
        )

        overlay.update_status("Getting it Done Done Done...")
        await self.show_main_content()

    async def show_main_content(self):
        """Fade out loading overlay and mount main UI."""
        overlay = self.query_one("#loading_overlay")
        overlay.styles.animate("opacity", 0.0, duration=1.0)
        overlay.set_timer(1.0, overlay.remove)

        content = self.query_one("#content")
        await content.mount_all(
            [
                NCHeader(id="Header", classes="header", user=self.profile_data.name),
                HorizontalScroll(
                    MainContainer(
                        id="book_list",
                        classes="book_list",
                        profile_data=self.profile_data,
                        book_data=self.book_data,
                        list_data=self.list_data,
                        prompt_data=self.prompt_data,
                        config_data=self.config_data,
                    ),
                    DetailsPanel(id="book_panel"),
                ),
                Footer(),
            ]
        )

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        panel = self.query_one("#book_panel", DetailsPanel)

        if isinstance(event.item, BookListItem):
            panel.update_details(event.item.book_data)

        if isinstance(event.item, ListListItem):
            panel.update_list_details(event.item.list_data, event.item.book_data)

        if isinstance(event.item, SeriesListItem):
            panel.update_series_details(SeriesBrlData(event.item.series_brl))

        if (
            isinstance(event.item, ProfilePublicListItem)
            or isinstance(event.item, ProfilePersonalListItem)
            or isinstance(event.item, ProfileBooksListItem)
        ):  # Example: load from your CSV, dict, or database
            panel.update_details(event.item.data)


class NCApp(App):
    def __init__(self, config_path: str, **kwargs):
        super().__init__(**kwargs)
        self.config_path = config_path
        self.config_data = Config(self.config_path)

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit NC"),
        Binding(key="r", action="read", description="Assign Read"),
        Binding(key="s", action="seriesAdd", description="Add Series"),
        Binding(key="p", action="promptAdd", description="Add Prompt"),
        Binding(key="l", action="listAdd", description="Add List"),
        Binding(key="H", action="hardRefesh", description="Hard Refresh Everything!"),
        Binding(key="h", action="help", description="Help Panel"),
    ]

    def action_help(self):
        """Show help modal."""
        self.push_screen(HelpModal())

    def action_seriesAdd(self):
        """Show modal for adding a series to local tracking"""
        self.push_screen(SeriesAddModal(title="series", config=self.config_data))

    def action_listAdd(self):
        """Show modal for adding a list to local tracking"""
        self.push_screen(ListAddModal(title="lists", config=self.config_data))

    def action_promptAdd(self):
        """Show modal for adding a prompt to local tracking"""
        self.push_screen(PromptAddModal(title="prompts", config=self.config_data))

    def action_read(self):
        """API move book from want-to-read to read"""
        self.push_screen(ReadModal())

    def on_mount(self) -> None:
        if not self.config_data.token and not self.config_data.email:
            self.push_screen(
                MissingConfigOption(
                    config_path=self.config_path, config_data=self.config_data
                )
            )
        else:
            self.push_screen(NCScreen(config_data=self.config_data))
