import requests
from get_quote import get_motivational_quote
from twilio.rest import Client
import os

API_KEY = os.environ.get('OWM_KEY')
SMS_WARM_TEXT = 'Get ready for the heat 😊 !'
SMS_COOL_TEXT = "Hope the cold doesn't bring you down 😢 !"
NAME = 'Swami'
TRIAL_NUMBER = '+13157137032'


# get latlong for the city
# city_name = input('Enter the name of your city as "City, Country')
city_name = 'Mumbai, India'
LATLONG_API = "https://geocode.maps.co/search"
LATLONG_PARAMS = {'q': city_name}
latlong_query = requests.get(url=LATLONG_API, params=LATLONG_PARAMS)
latlong_query.raise_for_status()
lat_location = latlong_query.json()[1]['lat']
lon_location = latlong_query.json()[1]['lon']

# get the weather for the city
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_PARAMS = {
    'lat': lat_location,
    'lon': lon_location,
    'appid': API_KEY,
    'units': 'metric'
}

weather = requests.get(url=WEATHER_URL, params=WEATHER_PARAMS)
weather.raise_for_status()
weather_dict = weather.json()
temp_data = weather_dict['main']
act_temp = temp_data['temp']
feel_temp = temp_data['feels_like']
temp_range = (temp_data['temp_max'], temp_data['temp_min'])
weather = weather_dict['weather'][0]['description']

warm = feel_temp >= 30
sms_text = f'{NAME} ! The temperature in {city_name} feels like {feel_temp} C with {weather.lower()}. '
sms_text += SMS_WARM_TEXT if warm else SMS_COOL_TEXT

quote, author = get_motivational_quote()
sms_text += f'\n\nQuote of the day:\n{quote}\n\t-{author}'
print(sms_text)


def send_sms(text):
    # Syntax obtained from https://www.twilio.com/docs/sms/quickstart/python
    # Set environment variables for your credentials. # Read more at http://twil.io/secure
    account_sid = os.environ["twilio_SID"]
    auth_token = os.environ["twilio_token"]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=text,
        from_="+13157137032",
        to=<MY NUMBER> #Insert destination number here
    )

    print(message.status)


send_sms(sms_text)

'''
{
	'coord': 
		{'lon': -74.4462, 
		'lat': 40.4968
		}, 
	'weather': [
			{'id': 800, 
			'main': 'Clear', 
			'description': 'clear sky', 
			'icon': '01d'
			}
			], 
	'base': 'stations', 
	'main': {
			'temp': 60.98, 
			'feels_like': 59.32, 
			'temp_min': 55.35, 
			'temp_max': 65.1, 
			'pressure': 1026, 
			'humidity': 54
			}, 
	'visibility': 10000, 
	'wind': 
		{'speed': 1.01, 
		'deg': 73, 
		'gust': 5.01
		}, 
	'clouds': {
			'all': 0
			}, 
	'dt': 1685104699, 
	'sys': {
		'type': 2, 
		'id': 2076514, 
		'country': 'US', 
		'sunrise': 1685093580, 
		'sunset': 1685146617
		}, 
	'timezone': -14400, 
	'id': 5101717, 
	'name': 'New Brunswick', 
	'cod': 200
}
'''
