import json
from datetime import datetime

# Казань 295954 
# Курск 293758
# Сочи 293687
# Москва 294021
# Калининград 292922

citykeys = {
   "Казань": "295954",
   "Курск": "293758",
   "Сочи": "293687",
   "Москва": "294021",
   "Калининград": "292922"
}

def format_date(date_str):
    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime("%d.%m.%Y")

# Функция ошибок не прощает
def test_get_weather(name, days=5): 
    weather_data = []
    with open(f"testApi/test_days/{name}.txt", "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    for day in data['DailyForecasts'][0:days]:
        date = format_date(day['Date'])
        temperature = {
        "min": day["Temperature"]["Minimum"]["Value"],
        "max": day["Temperature"]["Maximum"]["Value"]
        }
        text =  day['Day']['IconPhrase'],
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

