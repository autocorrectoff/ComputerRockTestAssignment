from django.apps import AppConfig
import os
from time import sleep
import requests
import json
from threading import Thread
from django.utils import timezone

class WeatherConfig(AppConfig):
    name = 'weather'
    open_weather_map_api_key = None

    def ready(self):
        module_dir = os.path.dirname(__file__)  
        file_path = os.path.join(module_dir, 'openweathermap_api_key.txt')
        with open(file_path, 'r') as fin:
            self.open_weather_map_api_key = fin.readline().strip()
        
        thread = Thread(target=self.__poll_open_weather_map_api)
        thread.start()

    def __poll_open_weather_map_api(self): 
        open_weather_map_api_url = f'http://api.openweathermap.org/data/2.5/weather?q=belgrade&appid={self.open_weather_map_api_key}'
        while(True):
            sleep(5 * 60) # fetch fresh data every 5 minutes
            r = requests.get(open_weather_map_api_url)
            if(r.status_code == 200):
                weather_info = self.__parse_weather_data(r.json())
                self.__store_weather_info(weather_info)
            else: 
                print('Could not fetch weather data')

    def __parse_weather_data(self, api_response):
        weather_info = {}
        weather_info['description'] = api_response['weather'][0]['description']
        weather_info['temperature'] = api_response['main']['temp']
        weather_info['visibility'] = api_response['visibility']
        weather_info['wind'] = api_response['wind']
        weather_info['last_update'] = timezone.now()

        return weather_info

    def __store_weather_info(self, weather_info):
        from .models import Weather
        weather = Weather(description=weather_info['description'], temperature=weather_info['temperature'], visibility=weather_info['visibility'], wind=json.dumps(weather_info['wind']), last_update=weather_info['last_update'])
        weather.save()