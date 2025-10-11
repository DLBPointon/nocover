from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.widgets import Label

from nocover.appinfo import APP_NAME, VERSION

class NCHeader(Horizontal):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def compose(self) -> ComposeResult:
        yield Label(
            f"Welcome to [b]{APP_NAME}[/] ([b]v{VERSION}[/]) {self.user}!",
            id="app-title"
        )
