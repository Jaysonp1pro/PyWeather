from textual.app import App
from textual.widgets import Button, Footer, Header, Static, Label
from textual.theme import Theme
from textual.containers import ScrollableContainer
import time

class TempDisplay(Static):
    pass

class WeatherInfoDisplay(Static):
    def compose(self):
        yield Label("Hello, world!", id="locationLabel")
        yield Button("Start", variant="success")
        yield Button("Stop", variant="warning")
        yield Button("Reset", variant="error")
        yield TempDisplay("0F")


class WeatherApp(App):
    CSS_PATH = "styles.css"
    
    def compose(self):

        yield Header(show_clock=True)
        yield Footer()

        with ScrollableContainer(id="WeatherInfoDisplay"):
            yield WeatherInfoDisplay()

    def on_mount(self) -> None:
        pass

if __name__ == "__main__":
    app = WeatherApp()
    app.run()