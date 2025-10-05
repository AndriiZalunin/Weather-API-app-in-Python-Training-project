import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.wind_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("weather-icon.png"))

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.wind_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        self.wind_label.setObjectName('wind_label')

        self.setStyleSheet("""
            QWidget {
                background-color: hsl(34, 84%, 87%);
            }
            QLabel {
                font-family: Arial;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit {
                font-size: 40px;
                border: 0px solid;
                border-radius: 25px;
                background-color: white;
            }
            QPushButton {
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border: 0px solid;
                border-radius: 25px;
                background-color: hsl(34, 100%, 66%);
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label {
                font-size: 50px;
            }
            QLabel#wind_label {
                font-size: 40px;
                font-family: Segoe UI emoji;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "3a757944ff44f3d45217cbb52d4389ac"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorised:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")



    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.wind_label.clear()

    def display_weather(self,data):
        temperature_Kelvin = data["main"]["temp"]
        temperature_Celsius = temperature_Kelvin - 273.15

        weathet_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        wind_direction = data["wind"]["deg"]

        self.temperature_label.setStyleSheet("font-size: 75px")
        self.emoji_label.setText(self.get_weather_emoji(weathet_id))
        self.temperature_label.setText(f"{temperature_Celsius:.1f}°C")
        self.description_label.setText(weather_description)
        self.wind_label.setText(self.get_wind(wind_speed, wind_direction))


    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <=232:
            return "⛈️"
        elif 300 <= weather_id <=321:
            return "🌦️"
        elif 500 <= weather_id <=531:
            return "🌧️"
        elif 600 <= weather_id <=622:
            return "❄️"
        elif 701 <= weather_id <=741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <=804:
            return "☁️"
        else:
            return ""

    @staticmethod
    def get_wind(wind_speed, wind_direction):
        wind_speed = f"{wind_speed} m/s"
        if (0 <= wind_direction <= 22.5) or (360-22.5 <= wind_direction <= 360):
            return wind_speed + "   ⬅️ E"
        elif 45+22.5 >= wind_direction >= 45-22.5:
            return wind_speed + "   ↙️ N-E"
        elif 90+22.5 >= wind_direction >= 90-22.5:
            return wind_speed + "   ⬇️ N"
        elif 135+22.5 >= wind_direction >= 135-22.5:
            return wind_speed + "   ↘️ N-W"
        elif 180+22.5 >= wind_direction >= 180-22.5:
            return wind_speed + "   ➡️ W"
        elif 225+22.5 >= wind_direction >= 225-22.5:
            return wind_speed + "   ↗️ S-W"
        elif 270+22.5 >= wind_direction >= 270-22.5:
            return wind_speed + "   ⬆️ S"
        elif 315+22.5 >= wind_direction >= 315-22.5:
            return wind_speed + "   ↖️ S-E"
        else:
            return ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())