# Weather API application (Training project)
## Overview

The program is designed to obtain certain weather data at a given moment
in a city specified by the user. The data is retrieved using an API from
the OpenWeather website: <https://openweathermap.org/>. The program 
interface was created using the `PyQt5` package.
## More detailed overview
The `PyQt5.QtWidgets` module is used to create the window and its components.
The elements are declared in the `__init__` function.
```Python
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
    #...
```
Next, in a separate function `initUI`, the window and all of the above elements are initialized.
This includes:
- the window name and icon;
- using the `QVBoxLayout` class
to place components;
- alignment using the `Qt` class;
- applying CSS for styling;
- binding a function to a button;

The `get_weather` function makes an API request based on the city name
that the user enters in LineEdit. Using the `request` package, we will receive 
data in JSON format if the request is successful. Otherwise, the `except` block
will call the `display_error` function and display a message in the program
window based on the status code of the error received.
```Python
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
    except:
        #...
```
If the `try` block is successfully executed, the `display_weather` function will be launched,
which will take the necessary data from the dictionary and print it using labels.
The static functions `get_weather_emoji` and `get_wind` are also called from here,
which supplement the information using emojis.
```Python
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
```