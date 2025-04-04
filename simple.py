from textual.app import App
from textual.widgets import Button, Footer, Header, Static, Label, Digits, Input
from textual.theme import Theme
from textual.containers import ScrollableContainer, Container
from textual import on
import time
import PyWeatherApi

Weather_Search_term = None

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
            with Container(id="top-side-container"):
                yield Label("Enter Town Name", id="enter-town-label")
                yield Input(placeholder="Town", type="text", max_length=50, id="town-input")
                yield Button("Search", variant="primary", id="search-button")

            with Container(id="bottom-side-container"):
                yield Label("Weather Results For Warne", id="weather-results-for-label")

                with Container(id="weather-results-container"):
                    with Container(classes="data-read-containers"):
                        yield Label("Temp:", classes="data-read-container-titles")
                        yield Digits("0 F", id="temp-reading", classes="data-read-container-digits")

                    with Container(classes="data-read-containers"):
                        yield Label("Humidity:", classes="data-read-container-titles")
                        yield Digits("0 %", id="humidity-reading", classes="data-read-container-digits")

        yield Footer()

    @on(Input.Submitted)
    @on(Button.Pressed)
    def update_search_term(self):
        input = self.query_one(Input)
        Weather_Search_term = input.value

        label = self.query_one("#weather-results-for-label")
        weather_data_container = self.query_one("#weather-results-container")
        
        coordinatesOfSearch = PyWeatherApi.request_coords(Weather_Search_term)
        if coordinatesOfSearch is None or coordinatesOfSearch.get("longitude") is None:
            label.update("Location not found!")
            weather_data_container.styles.display = "none"
            return

            
        temperature, humidity = PyWeatherApi.get_Weather(coordinatesOfSearch)
        if temperature is None:
            pass

        location_name = coordinatesOfSearch["name"]
        location_country = coordinatesOfSearch["country"]
        results_title_string = None
        if location_country is None:
            results_title_string = f"Weather Results For {location_name}"
        else:
            results_title_string = f"Weather Results For {location_name}, {location_country}"

        label.update(results_title_string)
        weather_data_container.styles.display = "block"

        temp_reading_widget = self.query_one("#temp-reading")
        temp_reading_widget.update(f"{temperature} F")

        humidity_reading_widget = self.query_one("#humidity-reading")
        humidity_reading_widget.update(f"{humidity} %")

    def on_mount(self) -> None:
        self.theme = "gruvbox"

if __name__ == "__main__":
    app = WeatherApp()
    app.run()