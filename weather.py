from const import APIKEY
from datetime import datetime
import requests
import json

def format_date(date_str):
    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime("%d.%m.%Y")

def get_weather(city, days):
    weather_data = []
    citykey = get_for_name(city)
    if citykey == 'err':
        return "error_city"

    data = get_weather_data(city=citykey)
    if data == "err":
        return "error_weather"

    for day in data['DailyForecasts'][0:days]:
        date = format_date(day['Date'])
        temperature = {"min": day["Temperature"]["Minimum"]["Value"], "max": day["Temperature"]["Maximum"]["Value"]}
        text = day['Day']['IconPhrase'],
        windSpeed = day['Day']['Wind']['Speed']['Value'],
        humidityAg = day['Day']['RelativeHumidity']['Average']
        
        weather_data.append({
            "date": date,
            "temperature": temperature,
            "text": text,
            "windSpeed": windSpeed,
            "humidityAg": humidityAg
        })
    return weather_data



def get_for_name(name):
    url = 'http://dataservice.accuweather.com/locations/v1/cities/search'
    params = {
        'q': name,
        'apikey': APIKEY
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    if response.status_code == 200:
        return data[0]['Key']
    else:
        print("---\nAPI-key error\n---")
        return "err"
    
def get_weather_data(city):
    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city}'
    params = {
        'apikey': APIKEY, 
        'details': 'true',
        'metric': 'true',
        'language': 'ru'
        }
    
    response = requests.get(url, params=params)

    data = response.json()
    if response.status_code == 200:
                return data
    else:
        print("---\nAPI-key error\n---")
        return "err"
    
print(get_weather("Казань", 1))