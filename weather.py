
import requests
def city_weather(city,date = None):
    API_KEY = "827951fef09f4e16af470732251607"
    current_url  = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
    

    response  = requests.get(current_url)
    response1 = requests.get(forecast_url)


    data  = response.json()  if response.status_code  == 200 else None
    data1 = response1.json() if response1.status_code == 200 else None
    return data,data1