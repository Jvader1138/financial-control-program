from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from screens import HomeScreen, RebalancerScreen, SettingsScreen

class Main(App):
    CSS_PATH = "styles/app.tcss"
    BINDINGS = [
        ("ctrl+s", "switch_screen('settings')", "Settings"),
        ("ctrl+home", "switch_screen('home')", "Home"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        # Register screens
        self.install_screen(HomeScreen(), name="home")
        self.install_screen(RebalancerScreen(), name="rebalancer")
        self.install_screen(SettingsScreen(), name="settings")
        self.push_screen("home")

def run() -> None:
    Main().run()

if __name__ == "__main__":
    run()
