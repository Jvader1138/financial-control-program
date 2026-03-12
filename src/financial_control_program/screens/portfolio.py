from screens import BaseScreen
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button
import yfinance as yf

class PortfolioScreen(BaseScreen):
    def compose_body(self) -> ComposeResult:
        yield Label("Stock Ticker:")
        yield Input(placeholder="VOO...", id="ticker")
        yield Button("Search", id="search")
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.switch_screen("home")
        elif event.button.id == "search":
            input_box = self.query_one("#ticker", Input)
            ticker = input_box.value.strip().upper()
            if not ticker:
                self.notify("Please enter a ticker symbol.", title="Error")
                return
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('regularMarketPrice')
            if current_price is None:
                self.notify(f"Could not fetch price for {ticker}", title="Error")
            else:
                self.notify(f"{ticker} Current Price: ${current_price}",title="Price")
            