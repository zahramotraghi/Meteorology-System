import datetime
import json
import urllib.request as urllib2

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Loading import Ui_Loading
from Input_Output import Ui_Input_Output

Counter = 30
check_city_name = False


# --------------------------------------------------------
class Root_Loading(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Loading()
        self.ui.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(50)
        self.show()


    def progress(self):
        global Counter
        self.ui.progressBar.setValue(Counter) 

        if Counter > 100:
            self.timer.stop()

            self.inout = Root_Input_Output()
            self.inout.show()
            self.close()

        Counter += 1


# --------------------------------------------------------
class Root_Input_Output(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Input_Output()
        self.ui.setupUi(self)

        self.clickFunc()
        self.show()


    def clickFunc(self) :
        self.ui.pushButton.clicked.connect(self.get_input)


    def get_input(self) : 
        self.cityName = self.ui.lineEdit_Name.text().strip()
        if self.cityName is None or self.cityName == '':
            QMessageBox.about(self, 'Error', 'Enter the name of a City!       ')
            return None

        try:
            urllib2.urlopen('https://www.google.com', timeout = 2)

        except urllib2.URLError: 
            QMessageBox.about(self, 'Error', 'Error: No internet!        ')
            return None     

        try:
            self.data1 = self.url_build(self.cityName)
            self.data2 = self.data_fetch(self.data1 )
            self.data3 = self.data_organize(self.data2)
            self.data4 = self.show_result(self.data3)

        except Exception:
            if check_city_name == False:
                QMessageBox.about(self, 'Error', 'The name of the city is wrong!        ')
                return None


    def url_build(self , city_name: str) -> str:


        #insert your APIKEY below
        self.api = ''
        self.city_name = city_name

        self.url1 = 'http://api.openweathermap.org/data/2.5/weather?q='
        self.url =  self.url1 + self.city_name + '&mode=json&units=metric&APPID=' + self.api

        return self.url


    def data_fetch(self , main_url: str) -> dict:
        self.main_url = main_url

        with urllib2.urlopen(self.main_url) as url:
            global check_city_name
            check_city_name = True

            self.result = url.read().decode('utf-8')
            self.dict1 = json.loads( self.result)
        return self.dict1        
    

    def data_organize(self , data1: dict) -> dict:
        self.main_data = data1

        self.main = self.main_data.get('main')
        self.sys = self.main_data.get('sys')
        self.data = dict(
            city = self.main_data.get('name'),
            country = self.sys.get('country'),
            temp = self.main.get('temp'),
            temp_max = self.main.get('temp_max'),
            temp_min = self.main.get('temp_min'),
            humidity = self.main.get('humidity'),
            pressure = self.main.get('pressure'),
            sky = self.main_data['weather'][0]['main'],
            sunrise = self.time_converte(self.sys.get('sunrise')),
            sunset = self.time_converte(self.sys.get('sunset')),
            wind = self.main_data.get('wind').get('speed'),
            dt = self.time_converte(self.main_data.get('dt')),
            cloudiness = self.main_data.get('clouds').get('all')
        )
        return self.data


    def time_converte(self , time: int) -> str:
        self.time = time
        self.converted_time = datetime.datetime.fromtimestamp(int(self.time)).strftime('%H:%M:%S')
        return self.converted_time    


    def show_result(self ,data: dict):
        self.data = data

        self.ui.label_11.setText ('Current weather in {} , {}:'.format(data['city'], data['country']))
        self.ui.label_12.setText ('Temp: {} °C  ,  {}' .format(data['temp'], data['sky']))
        self.ui.label_13.setText ('Min temp: {} °C  ,  Max temp: {} °C'.format(data['temp_min'], data['temp_max']))
        self.ui.label_14.setText ('Wind speed: {} meter/sec'.format(data['wind']))
        self.ui.label_15.setText ('Humidity: %{}'.format(data['humidity']))
        self.ui.label_16.setText ('Cloud: %{}'.format(data['cloudiness']))
        self.ui.label_17.setText ('Pressure: {} hPa'.format(data['pressure']))
        self.ui.label_18.setText ('Sunrise at: {}  ,  Sunset at: {}'.format(data['sunrise'] , data['sunset'] ))
        self.ui.label_20.setText ('Last update: {}'.format(data['dt']))


# --------------------------------------------------------
if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)  
    Root = Root_Loading()
    sys.exit(app.exec_())