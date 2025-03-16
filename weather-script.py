import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the window
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 300, 150)

        # Create widgets
        self.city_label = QLabel("Enter City Name:")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")
        self.weather_info_label = QLabel("Weather information will appear here.")

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.weather_info_label)
        self.setLayout(layout)

        # Connect button click to the function
        self.get_weather_button.clicked.connect(self.fetch_weather)

    def fetch_weather(self):
        # Get the city name from the input field
        city = self.city_input.text().strip()

        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        # Replace 'your_api_key_here' with your actual OpenWeatherMap API key
        api_key = "Enter api key"  # Ensure this is your valid API key
        base_url = "http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={api_key}"  # Correct base URL
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Use 'imperial' for Fahrenheit
        }

        try:
            # Make the API request
            response = requests.get(base_url, params=params)

            # Handle HTTP errors
            if response.status_code == 200:
                # Parse the JSON response
                weather_data = response.json()

                # Extract relevant information
                main = weather_data["main"]
                weather = weather_data["weather"][0]

                # Display the weather information
                weather_info = (
                    f"Weather in {city}:\n"
                    f"Temperature: {main['temp']}°C\n"
                    f"Humidity: {main['humidity']}%\n"
                    f"Weather Condition: {weather['description']}"
                )
                self.weather_info_label.setText(weather_info)
            elif response.status_code == 401:
                error_message = "Error: Unauthorized. Please check your API key."
                self.weather_info_label.setText(error_message)
                QMessageBox.critical(self, "API Error", error_message)
            else:
                error_message = f"Error: Unable to fetch weather data (HTTP {response.status_code})"
                self.weather_info_label.setText(error_message)
                QMessageBox.critical(self, "API Error", error_message)
        except Exception as e:
            # Handle exceptions (e.g., network issues)
            error_message = f"An error occurred: {str(e)}"
            self.weather_info_label.setText(error_message)
            QMessageBox.critical(self, "Error", error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
