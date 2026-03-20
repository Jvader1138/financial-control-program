import sqlite3
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button
from textual.containers import Container, Horizontal

class EditRowScreen(ModalScreen):
    def __init__(self, row_data):
        super().__init__()
        self.row_data = row_data

    def compose(self) -> ComposeResult:
        with Container(id="modal-edit-row"):
            yield Label("Ticker")
            yield Input(value=self.row_data[0], disabled=True, id="ticker")
            yield Label("Price")
            yield Input(value=self.row_data[1], disabled=True, id="price")
            yield Label("Count")
            yield Input(value=self.row_data[2], id="count")
            yield Label("Total Value")
            yield Input(value=self.row_data[3], disabled=True, id="total_value")
            yield Label("Target")
            yield Input(value=self.row_data[4], id="target_percent")
            yield Label("", id="error")
            with Horizontal():
                yield Button("Save", variant="success", id="save", classes="button--margin")
                yield Button("Back", variant="error", id="back", classes="button--margin")

    def on_mount(self) -> None:
        self.query_one("#error").visible = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss(False)
        elif event.button.id == "save":
            try:
                new_count = self.query_one("#count", Input)
                new_count_value = round(float(new_count.value), 3)
                new_target_percent = self.query_one("#target_percent", Input)
                new_row = (
                    new_count_value,
                    round(float(self.row_data[1]) * new_count_value, 2),
                    int(new_target_percent.value),
                    self.row_data[0]
                )
            except Exception as e:
                error_label = self.query_one("#error", Label)
                error_label.update(f"{e}")
                error_label.visible = True
                return
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE portfolio SET count = ?, total_value = ?, target_percent = ? WHERE ticker = ?", new_row)
            conn.commit()
            conn.close()
            self.dismiss(True)
            