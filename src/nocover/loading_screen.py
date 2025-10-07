from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

class LoadingScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("⏳ Loading... Please wait.")
