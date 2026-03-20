from textual.app import App
from screens import HomeScreen, PortfolioScreen, SettingsScreen
import sqlite3

class Main(App):
    CSS_PATH = "styles/app.tcss"
    TITLE = "Financial Control Program"
    BINDINGS = [
        ("ctrl+s", "switch_screen('settings')", "Settings"),
        ("ctrl+home", "switch_screen('home')", "Home"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        # Fetch data
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS portfolio (
            ticker TEXT PRIMARY KEY,
            price NUMERIC,
            count NUMERIC,
            total_value NUMERIC,
            target_percent INTEGER
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()
        # Register screens
        self.install_screen(HomeScreen(), name="home")
        self.install_screen(PortfolioScreen(), name="portfolio")
        self.install_screen(SettingsScreen(), name="settings")
        self.push_screen("home")

def run() -> None:
    Main().run()

if __name__ == "__main__":
    run()
