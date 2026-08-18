
import os
import requests
from dotenv import load_dotenv
import psycopg2


load_dotenv()

WeatherAPI = os.getenv('WEATHER_API_KEY')
DBPASSWORD = os.getenv('DATABASE_PASSWORD')

print(f'{WeatherAPI}')

city = "Baku"
countryCode = "AZ"


try:
    geoResponse = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{countryCode}&appid={WeatherAPI}")
    geoResponse.raise_for_status()

except requests.exceptions.RequestException as error:

    print(f"An error occured {error}")

print(f'*** Geolocation information successfully extracted: {city},{countryCode} *** ')
geoJson = geoResponse.json()[0]

lat = geoJson['lat']
lon = geoJson['lon']

print(f'lat = {lat} & lon = {lon}')


try:
    weatherResponse = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WeatherAPI}")

except requests.exceptions.RequestException as error:
    print(f'An error occured {error}')

print(f'*** Weather information successfully pulled *** ')


conn = psycopg2.connect(
        host = "aws-0-ap-northeast-1.pooler.supabase.com",
        dbname = "postgres",
        user = "postgres.emsqizzjlsqcmorvcwyd", 
        password = f'{DBPASSWORD}',
        port = 5432,
        sslmode = "require"
)


curr = conn.cursor()


weatherJSON = weatherResponse.json()

temp = weatherJSON['main']['temp']
humidity = weatherJSON['main']['humidity']
weather_condition = weatherJSON['weather'][0]['description']
recorder_at = weatherJSON['dt']


print(temp,humidity,weather_condition)



curr.execute(f"INSERT INTO raw.weather_readings (city,temp,humidity,weather_condition,recorded_at,ingested_at) \
             VALUES ('{city}', {temp}, {humidity}, '{weather_condition}', to_timestamp({recorder_at}), now())")

conn.commit()
curr.close()
conn.close()


