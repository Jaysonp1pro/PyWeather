from textual.app import App
from textual.widgets import Button, Footer, Header, Static, Label
from textual.theme import Theme
from textual.containers import ScrollableContainer, Container
import time

class TempDisplay(Static):
    pass

class WeatherInfoDisplay(Static):
    def compose(self):
        yield Button("Start", variant="success")
        yield Button("Stop", variant="warning")
        yield Button("Reset", variant="error")
        yield TempDisplay("0F")


class WeatherApp(App):
    CSS_PATH = "styles.css"
    
    def compose(self):

        yield Header(show_clock=True)

        with Container(id="app-grid"):
            with Container(id="left-side-container"):
                yield Label("Hello, world!", id="locationLabel")

            with Container(id="right-side-container"):
                yield Label("idk lol")


        yield Footer()

    def on_mount(self) -> None:
        pass

if __name__ == "__main__":
    app = WeatherApp()
    app.run()