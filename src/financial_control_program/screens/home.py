from screens import BaseScreen
from textual.app import ComposeResult
from textual.widgets import Static, Button

class HomeScreen(BaseScreen):
    def compose_body(self) -> ComposeResult:
        yield Static("Home", id="title")
        yield Button("Open Settings", id="open-settings")
        yield Button("Open Portfolio", id="open-portfolio")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open-settings":
            self.app.switch_screen("settings")
        elif event.button.id == "open-portfolio":
            self.app.switch_screen("portfolio")
