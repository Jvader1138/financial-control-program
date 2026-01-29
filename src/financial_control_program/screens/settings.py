from screens import BaseScreen
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button

class SettingsScreen(BaseScreen):
    def compose_body(self) -> ComposeResult:
        yield Label("Greeting prefix:")
        yield Input(placeholder="Hello / Howdy / Hi", id="greeting")
        yield Button("Save", id="save")
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.switch_screen("home")
        elif event.button.id == "save":
            # Save to config service (left as an exercise)
            self.notify("Saved!", title="Settings")
            