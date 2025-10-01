# General Package Imports
import os
import json

# Textual Package Import
from textual.app import App, ComposeResult
from textual.screen import ModalScreen, Screen
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, HorizontalScroll,VerticalScroll
from textual.widgets import Label, TabbedContent, TabPane, ListView
from textual.widgets import Footer, Button, Input, Static, Link

# Local App Imports
from nocover.appinfo import VERSION, APP_NAME
from nocover.config import Config
from nocover.list_items import BookListItem, SeriesListItem, ListListItem, PromptListItem, ProfilePublicListItem, ProfileBooksListItem, ProfilePersonalListItem

# Local App Modal Imports
# from nocover.modals.start_up import StartUp
from nocover.modals.help_page import HelpModal
from nocover.modals.error_page import ErrorModal
from nocover.modals.series_add_modal import SeriesAddModal

# Local App Hardcover Imports
from nocover.hardcover.raw_queries import HARDCOVER_PROFILE_QUERY
from nocover.hardcover.raw_queries import HARDCOVER_USER_BOOKS_BY_STATUS
from nocover.hardcover.get_profile import Profile
from nocover.hardcover.get_books import BookData as UserBookData
from nocover.hardcover.get_series import SeriesData

DEFAULT_BOOK_COVER = """
+-------------+
|   📘 ???    |
|             |
|   No Img    |
| Support Yet |
+-------------+
"""


# TODO: Refactor into StartUp
class MissingConfigOption(ModalScreen[None]):
    """

    """
    def __init__(
        self,
        config_path: str,
        profile_data: Profile,
        book_data: UserBookData,
        config_data: Config
    ) -> None:
        super().__init__()
        self.config_path: str           = config_path
        self.config_data: Config        = config_data
        self.profile_data: Profile      = profile_data
        self.book_data: UserBookData    = book_data
        self.config_input: Input        = Input(
            placeholder = "Hardcover Token"
        )
        self.email_input: Input         = Input(
            placeholder = "eto_demerzel@trantor.empire"
        )


    def compose(self) -> ComposeResult:
        with Vertical(classes="popup"):
            yield Label(
                "Config file missing. Please enter your Hardcover API Token:"
            )
            yield self.config_input

            yield Label("It's helpful to have your email too!")
            yield self.email_input

            with Horizontal():
                yield Button("Save", id="save", variant="success")
                yield Button("Cancel", id="cancel", variant="error")

    # TODO: NEED TO ADD VALIDATION OF INPUT
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":

            os.makedirs(
                os.path.dirname(self.config_path), exist_ok=True
            )
            with open(self.config_path, "w") as f:
                data: dict[str, str] = {
                    "HARDCOVER_API_TOKEN"   : self.config_input.value,
                    "EMAIL"                 : self.email_input.value
                }

                # fp is the File to Process... probably not the official
                # meaning but it works
                json.dump(
                    obj= data,
                    fp=f,
                    encoding='utf-8',
                    sort_keys = True,
                    indent=4 # HARD MUST, NO 2 SPACE INDENTS
                )

            self.app.pop_screen()
            self.app.push_screen(
                NCScreen(
                    self.profile_data,
                    self.book_data,
                    self.config_data
                )
            )  # go to main screen

        elif event.button.id == "cancel":
            self.app.exit("User cancelled config setup.")


class Header(Horizontal):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.title      = "Header Application"
        self.sub_title  = "With title and sub-title"

    def compose(self) -> ComposeResult:
        yield Label(
            f"Welcome to [b]{APP_NAME}[/] ([b]v{VERSION}[/]) {self.user}!",
            id="app-title"
        )


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
            yield Static(
                content=DEFAULT_BOOK_COVER, id="book_cover", markup=False
            )

            # Right container is the details container we can fill dynamically
            yield VerticalScroll(id="details_rows")


    def update_series_details(self, data: SeriesData) -> None:
        """Update panel with ListItem per book in SeriesData."""
        container = self.query_one("#details_rows", VerticalScroll)
        container.remove_children()

        # --- Series Card ---
        series_block = Vertical(classes="detail-series")

        series_name = data.series_data["Series"].get(
            "@Name", "Unknown Series"
        )
        series_block.border_title = (
            f"Series overview: [b][u]{series_name}[/u][/b]"
        )

        container.mount(series_block)

        universe_tag = data.series_data["Series"].get(
            "Universe", "Series is a standalone!"
        )

        universe_tag = (
            f"Series belongs to the {universe_tag["@Name"]} Universe {
                (
                    ""
                    if universe_tag["@Position"] is None
                    else f"(Position: {universe_tag["@Position"]})"
                )
            }"
            if universe_tag != "Series is a standalone!"
            else universe_tag
        )

        series_block.mount(Horizontal(*[
            Label(universe_tag)], classes="detail-row")
        )

        database_info = data.series_data["Series"]["Database"]
        series_block.mount(Horizontal(*[
            Label("Database: ", classes="detail-key"),
            Link(
                str(f"{database_info["@Name"]}/{database_info["@Item"]}"),
                url=f"https://hardcover.app/series/{database_info["@Item"]}",
                tooltip=f"Head to Hardcover page for {series_name}"
            )
        ], classes="detail-row"))

        series_description = data.series_data["Series"]["Description"]
        series_description = str(series_description)
        series_block.mount(
            Horizontal(
                *[
                    Label("Description: ", classes="detail-key"),
                    Label(series_description, classes="multi-line-box")
                ],
                classes="detail-row"
            )
        )

        # --- Book Cards ---
        books = data.series_data["Books"]["Book"]
        if isinstance(books, dict):  # handle single-book edge case
            books = [books]

        for idx, book in enumerate(books, start=1):

            # Mount the book_block container with key information as title
            book_block = Vertical(classes="detail-book")
            book_name = book.get('@Name','Unknown')
            book_position = book.get('@Position', 'Unknown')
            book_block.border_title = (
                f"Book {idx} -:- {book_name} -:- Position: {book_position}"
            )
            container.mount(book_block)

            # Add rows into the book_block
            for key, value in book.items():

                if key == "Tag":
                    value = "\n".join(value)

                # Skip these from the outputs
                if key not in ["@Name", "@Position"]:
                    new_key = key.replace("@", "")

                    row = Horizontal(
                        Label(
                            f"{new_key}: ".title(),
                            classes="detail-key"
                        ),
                        (
                            Label(
                                value,
                                classes=(
                                    "detail-value"
                                    if len(str(value)) < 60
                                    else "detail-value-big"
                                )
                            )
                            if new_key != "Database" else
                            Link(
                                f"{value["@Name"]}/{value["@Item"]}",
                                url=f"https://hardcover.app/books/{value["@Item"]}",
                                tooltip=f"Head to Hardcover page for {book_name}"
                            )
                        ),
                        classes="detail-row"
                    )
                    book_block.mount(row)



    def update_details(self, data: dict):
        """
        Update panel with arbitrary key:value pairs from `data`.
        Returns a DataTable containing rows of key: value formatted
        somewhat nicely.
        """
        ascii_text = data.pop("book_cover", DEFAULT_BOOK_COVER)
        self.query_one("#book_cover", Static).update(ascii_text)

        container = self.query_one("#details_rows", VerticalScroll)
        container.remove_children()

        if not data:
            return

        # This is smart, i should use this again elsewhere
        max_key_len: int = max(len(k) for k in data.keys())

        # get list of keys in dict, and re-order so description is last
        key_list = list(data.keys())
        for i in ["description", "slug"]:
            key_list.remove(i)
        key_list.append("description")

        for key in key_list:
        # for key, value in data.items():
            # create row and mount it into the container first
            row: Horizontal = Horizontal(classes="detail-row")
            container.mount(row)

            new_key = " ".join(key.split("_"))

            # now we can mount children into the row

            row.mount(
                Label(
                    f"{new_key.ljust(max_key_len + 2).title()}",
                    classes="detail-key")
            )

            # The join/split attempts to remove some of the double spacing
            # going on in the large text fields
            if key == "book_series":
                info = [i["series"]["name"] for i in data[key] if i["series"]]
                info = ( "None" if len(info) < 1 else info )
            else:
                info = data[key]

            if key == "title":

                row.mount(
                    Link(
                        str(info),
                        url=f"https://hardcover.app/books/{data["slug"]}",
                        tooltip=f"Head to Hardcover page for {info}"
                    )
                )

            else:

                row.mount(
                    Label(
                        content=str(info),
                        classes="multi-line-box-2",
                        markup=True)
                )


class MainContainer(TabbedContent):
    def __init__(
        self,
        profile_data: Profile,
        book_data: UserBookData,
        config_data: Config,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.profile_data = profile_data
        self.book_data = book_data
        self.border_title = "Data Panel"
        self.config_data = config_data
        self.book_by_Status = book_data.dict_by_status


    @staticmethod
    def createListListItem():
        return [
            ListListItem(
                 line
            ) for line in open("./hi/lists.csv")
        ]

    @staticmethod
    def createPromptListItem():
        return [
            PromptListItem(
                line
            ) for line in open("./hi/prompt_list.csv")
        ]


    @staticmethod
    def createProfileListItem(profile_data):
        return [
            ProfilePublicListItem(
                profile_data
            ),
            ProfileBooksListItem(
                profile_data
            ),
            ProfilePersonalListItem(
                profile_data
            )
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
                            "Add",
                            id="add_series",
                            classes="general-button"
                        )
                        yield Button(
                            "Refresh",
                            id="refresh_active",
                            classes="general-button"
                        )
                        yield Button(
                            "Remove",
                            id="remove_series",
                            classes="general-button",
                            disabled=True
                        )
                yield ListView(
                    *[
                        SeriesListItem(
                            series_name=line.split(',')[0],
                            series_count=str(line.split(',')[1]),
                            series_brl=line.split(',')[2]
                        ) for line in open("./hi/series_list.csv")
                    ],
                    id="series_list"
                )

            with TabPane(title="Lists", id="list_list"):
                yield ListView(
          		    *self.createListListItem(),
          		    id = "ListList"
          		)

            with TabPane(title="Prompts", id="list_prompt"):
                yield ListView(
                    *self.createPromptListItem(),
                    id = "SeriesList"
                )

            with TabPane(title="Profile", id="profile_page"):
                yield ListView(
                    *self.createProfileListItem(
                        self.profile_data
                    ),
                    id='list_view_profile'
                )


    def refresh_series_list(self):
            """Reload the series list from the CSV file."""

            # if active.pane == series
            series_list = self.query_one("#series_list", ListView)
            series_list.clear()

            with open("./hi/series_list.csv") as f:
                for line in f:
                    if not line == "\n":
                        name, count, brl = line.strip().split(",")

                        # Doesn't actually get triggered... annoyingly
                        if not os.path.exists(brl.strip()):
                            ErrorModal(f"BRL file does not exist for: {name}")

                        series_list.append(
                            SeriesListItem(
                                series_name=name,
                                series_count=str(count),
                                series_brl=brl
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
        csv_file = "./hi/series_list.csv"
        with open(csv_file, "r") as f:
            lines = f.readlines()

        # make tmp file
        with open(".series_list.csv", "w") as n:
            for line in lines:
                if not line == f"{series_name},{series_count},{series_brl}":
                    n.write(line)

        # remove original, cp tmp over it
        os.remove(csv_file)
        os.rename(".series_list.csv", csv_file)
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
            self.app.push_screen(SeriesAddModal(self.config_data))
        elif event.button.id == "remove_series":
            self.remove_series()


class NCScreen(Screen):
    def __init__(self,
        profile_data: Profile,
        book_data: UserBookData,
        config_data: Config
    ):
        super().__init__()
        self.profile_data = profile_data
        self.book_data = book_data
        self.config_data = config_data

    CSS_PATH = "layout.tcss"

    def compose(self) -> ComposeResult:
        yield Header(
            id="Header",
            classes="header",
            user=self.profile_data.name
        )

        with HorizontalScroll():
                yield MainContainer(
                    id="book_list",
                    classes="book_list",
                    profile_data=self.profile_data,
                    book_data=self.book_data,
                    config_data=self.config_data
                )

                yield DetailsPanel(
                    id="book_panel"
                )

        yield Footer()


    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        panel = self.query_one("#book_panel", DetailsPanel)

        if isinstance(event.item, BookListItem):
            panel.update_details(event.item.book_data)

        if isinstance(event.item, SeriesListItem):
            panel.update_series_details(SeriesData(event.item.series_brl))

        if (
            isinstance(event.item, ProfilePublicListItem)
            or isinstance(event.item, ProfilePersonalListItem)
            or isinstance(event.item, ProfileBooksListItem)
        ):            # Example: load from your CSV, dict, or database
            panel.update_details(event.item.data)


class NCApp(App):
    def __init__(self, config_path: str, **kwargs):
        super().__init__(**kwargs)
        self.config_path = config_path
        self.config_file = self.config_path + "/configs.json"
        self.config_data = Config(self.config_path)

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit NC"),
        Binding(
            key="r",
            action="read",
            description="Assign Read"
        ),
        Binding(
            key="s",
            action="seriesAdd",
            description="Add Series"
        ),
        Binding(
            key="h", action="help", description="Help Panel"
        )
    ]

    def action_help(self):
        """Show help modal."""
        self.push_screen(HelpModal())

    def action_seriesAdd(self):
        """Show modal for adding a series to local tracking"""
        self.push_screen(SeriesAddModal(self.config_data))

    def action_read(self):
        """API move book from want-to-read to read"""
        pass

    def on_mount(self) -> None:
        offline = False
        profile_data = Profile(
            HARDCOVER_PROFILE_QUERY, self.config_data, offline
        )
        book_data = UserBookData(
            HARDCOVER_USER_BOOKS_BY_STATUS, self.config_data, offline
        )

        if not os.path.exists(self.config_path):
            self.push_screen(
                MissingConfigOption(
                    config_path = self.config_path,
                    config_data = self.config_data,
                    profile_data = profile_data,
                    book_data = book_data
                )
            )
        else:
            self.push_screen(
                NCScreen(
                    profile_data,
                    book_data,
                    config_data = self.config_data
                )
            )
