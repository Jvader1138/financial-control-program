from textual.screen import Screen
from textual.widgets import Header, Footer

class BaseScreen(Screen):
    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield from self.compose_body()

    def compose_body(self):
        yield ""
