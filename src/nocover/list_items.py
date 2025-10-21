from textual.widgets import ListItem, Label

from nocover.hardcover.get_profile import Profile


class BookListItem(ListItem):
    def __init__(self, book_data: dict[str, str]):
        self.name = book_data["title"]
        super().__init__(Label(self.name))
        self.book_data = book_data


class SeriesListItem(ListItem):
    def __init__(self, series_name: str, series_count: str, series_brl: str):
        super().__init__(Label(f"{series_name} ({series_count})", markup=True))
        self.series_name = series_name
        self.series_count = series_count
        self.series_brl = series_brl


class ListListItem(ListItem):
    def __init__(self, slug: str, name: str, list_data: dict[str, str]):
        super().__init__(Label(name))
        self.list_name = name
        self.list_slug = slug
        self.list_data = list_data["list_information"]
        self.book_data = list_data["book_list"]


class PromptListItem(ListItem):
    def __init__(self, prompt: str):
        super().__init__(Label(prompt))
        self.prompt_name = prompt


class ProfilePublicListItem(ListItem):
    def __init__(self, profile: Profile):
        super().__init__(Label("Users Info"))
        self.data = profile.public_data_dict


class ProfileBooksListItem(ListItem):
    def __init__(self, profile: Profile):
        super().__init__(Label("Users Books Info"))
        self.data = profile.book_data_dict


class ProfilePersonalListItem(ListItem):
    def __init__(self, profile: Profile):
        super().__init__(Label("Users Personal Info"))
        self.data = profile.private_data_dict
