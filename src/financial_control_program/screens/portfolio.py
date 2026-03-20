from screens import BaseScreen, EditRowScreen
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, DataTable
from textual.containers import Vertical, Horizontal
import sqlite3
import yfinance as yf

def get_styled_row(ticker, price, count, total_value, target_percent):
    return [
        ticker,
        Text(f"{price:.2f}", justify="right"),
        Text(f"{count:.3f}", justify="right"),
        Text(f"{total_value:.2f}", justify="right"),
        Text(f"{target_percent}%", justify="right")
    ]

class PortfolioScreen(BaseScreen):
    def compose_body(self) -> ComposeResult:
        yield Static("Portfolio", id="title")

        with Horizontal():
            yield Input(placeholder="Enter ticker (e.g. VOO)", id="ticker_input")
            yield Button("Add", id="add_stock")

        with Vertical(id="portfolio_container"):
            yield DataTable(id="portfolio_table")
            
        with Horizontal():
            yield Button("Update", id="update", classes="button--margin")
            yield Button("Save", variant="success", id="save", classes="button--margin")
            yield Button("Back", variant="error", id="back", classes="button--margin")

    def on_mount(self) -> None:
        # Create DataTable
        table = self.query_one("#portfolio_table", DataTable)
        table.add_column("Ticker", key="ticker")
        table.add_column("Price", key="price")
        table.add_column("Count", key="count")
        table.add_column("Total Value", key="total_value")
        table.add_column("Target", key="target_percent")
        table.cursor_type = "row"
        self.reset_table()        
    
    def reset_table(self) -> None:
        table = self.query_one("#portfolio_table", DataTable)
        table.clear()
        # Fetch data
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ticker, price, count, total_value, target_percent FROM portfolio;")
        self.portfolio_data = cursor.fetchall()
        conn.close()
        # Populate data
        for row in self.portfolio_data:
            table.add_row(*get_styled_row(row[0], row[1], row[2], row[3], row[4]), key=row[0])
    
    def get_share_price(self, ticker: str):
        stock = yf.Ticker(ticker)
        price = stock.info.get("regularMarketPrice")
        if price is None:
            self.notify(f"Could not fetch price for {ticker}", title="Error", severity="error")
        else:
            return round(price, 2)
        
    def update_all_prices(self) -> None:
        new_portfolio = []
        for row in self.portfolio_data:
            new_price = self.get_share_price(row[0])
            new_portfolio.append((row[0], new_price, row[2], round(new_price * row[2], 2), row[4]))
        self.portfolio_data = new_portfolio
        table = self.query_one("#portfolio_table", DataTable)
        table.clear()
        for row in self.portfolio_data:
            table.add_row(*get_styled_row(row[0], row[1], row[2], row[3], row[4]), key=row[0])
        self.notify("All share prices have been updated")
        
    def get_row_pos(self, ticker: str):
        primary_keys = [x[0] for x in self.portfolio_data]
        return primary_keys.index(ticker) if ticker in primary_keys else None
    
    def add_or_replace_row(self, ticker, price, count, total_value, total_percent) -> None:
        table = self.query_one("#portfolio_table", DataTable)
        del_pos = self.get_row_pos(ticker)
        if del_pos is not None:
            self.portfolio_data.pop(del_pos)
        self.portfolio_data.append((ticker, price, count, total_value, total_percent))
        if ticker in table.rows.keys():
            table.remove_row(ticker)
        table.add_row(*get_styled_row(ticker, price, count, total_value, total_percent), key=ticker)
    
    def save_rows(self) -> None:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.executemany("INSERT OR REPLACE INTO portfolio VALUES (?, ?, ?, ?, ?)", self.portfolio_data)
        conn.commit()
        conn.close()
        self.notify("Portfolio saved")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.switch_screen("home")
        elif event.button.id == "add_stock":
            ticker_input = self.query_one("#ticker_input", Input)
            ticker = ticker_input.value.strip().upper()
            if ticker:
                price = self.get_share_price(ticker)
                if price:
                    self.add_or_replace_row(ticker, price, 0, 0, 0)
                    ticker_input.value = ""
            else:
                self.notify("Please enter a ticker symbol", title="Error", severity="warning")
        elif event.button.id == "save":
            self.save_rows()
        elif event.button.id == "update":
            self.update_all_prices()
    
    def handle_modal_result(self, result: bool) -> None:
        if result:
            self.notify("Row saved")
            self.reset_table()

    @on(DataTable.RowSelected)
    def on_row_selected(self, event: DataTable.RowSelected) -> None:
        row_key = event.row_key
        pos = self.get_row_pos(row_key)
        if pos is not None:
            row_data = self.portfolio_data[(pos)]
            row_data_str = (
                row_data[0],
                str(row_data[1]),
                str(row_data[2]),
                str(row_data[3]),
                str(row_data[4])
            )
            self.app.push_screen(EditRowScreen(row_data_str), self.handle_modal_result)
