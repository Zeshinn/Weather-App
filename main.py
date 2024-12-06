import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel
                             , QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temprature_label = QLabel("", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temprature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temprature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        
        # Ensure description_label content is centered
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temprature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")

        # Set the description label to a larger fixed size
        self.description_label.setFixedSize(200, 200)

        self.setStyleSheet("""
                            QLabel, QPushButton{
                                font-family: calibri;              
                            }
                            QLabel#city_label{
                                font-size: 40px;
                                font-style: italic;               
                            }
                            QLineEdit#city_input{
                                font-size: 40px;
                            }
                           QPushButton#get_weather_button{
                                font-size: 30px;
                                font-weight: bold;
                           }
                           QLabel#temperature_label{
                                font-size: 75px;
                                
                           }
                           QLabel#description_label{
                                font-size: 50px;
                           }

        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "ad76e4e54acf461d8f9125634240612" # yeah I know
        city = self.city_input.text()

        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        response = requests.get(url)
        code = response.status_code
        if code == 200:
            data = response.json()
            self.display_weather(data)
        else:
            self.display_error()
    
    def display_error(self):
        self.temprature_label.setText("Not valid!")

    def display_weather(self, data):
        self.temprature_label.setText(f"{data['current']['temp_c']}°C")
        icon_url = f"http:{data['current']['condition']['icon']}"
        response = requests.get(icon_url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).read())
            pixmap = pixmap.scaled(self.description_label.width(),
                                   self.description_label.height(),
                                   Qt.KeepAspectRatio, 
                                   Qt.SmoothTransformation)

            self.description_label.setPixmap(pixmap)
        else:
            self.description_label.setText("Image not available")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
