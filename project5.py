import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env from the same folder as project5.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

API_KEY = os.getenv("OPENWEATHER_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Cache current weather for five minutes.
weather_cache = {}
CACHE_SECONDS = 300


def get_current_weather(city):
    city_key = city.strip().lower()
    now = time.time()

    if city_key in weather_cache:
        saved_time, saved_data = weather_cache[city_key]
        if now - saved_time < CACHE_SECONDS:
            print("\nUsing cached weather data.")
            return saved_data

    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            print("City not found. Check the spelling.")
            return None

        if response.status_code == 401:
            print("Invalid or inactive API key. Check your .env file.")
            return None

        response.raise_for_status()
        data = response.json()

        weather_cache[city_key] = (now, data)
        return data

    except requests.exceptions.RequestException as error:
        print(f"Network or API error: {error}")
        return None


def get_forecast(city):
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            print("Forecast city not found.")
            return None

        if response.status_code == 401:
            print("Invalid or inactive API key.")
            return None

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"Could not retrieve forecast: {error}")
        return None


def display_weather(data):
    name = data.get("name", "Unknown city")
    main = data.get("main", {})
    weather_list = data.get("weather", [])
    wind = data.get("wind", {})

    description = (
        weather_list[0].get("description", "Unavailable")
        if weather_list else "Unavailable"
    )

    print("\n" + "=" * 42)
    print(f"CURRENT WEATHER: {name}")
    print("=" * 42)
    print(f"Temperature : {main.get('temp', 'N/A')} °C")
    print(f"Feels like  : {main.get('feels_like', 'N/A')} °C")
    print(f"Humidity    : {main.get('humidity', 'N/A')}%")
    print(f"Conditions  : {description.title()}")
    print(f"Wind speed  : {wind.get('speed', 'N/A')} m/s")
    print("=" * 42)


def display_forecast(data):
    if not data or not data.get("list"):
        print("Forecast is unavailable.")
        return

    # Select one forecast near midday for each date.
    daily = {}

    for item in data["list"]:
        date_text = item.get("dt_txt", "")
        if not date_text:
            continue

        date = date_text.split(" ")[0]
        hour = date_text.split(" ")[1][:2]

        if date not in daily:
            daily[date] = item

        if hour == "12":
            daily[date] = item

    print("\nFIVE-DAY FORECAST")
    print("-" * 65)
    print(f"{'Date':<13} {'Temp (C)':<12} {'Conditions'}")
    print("-" * 65)

    for date, item in list(daily.items())[:5]:
        temp = item.get("main", {}).get("temp", "N/A")
        conditions = item.get("weather", [{}])[0].get(
            "description", "Unavailable"
        )
        try:
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y")
        except ValueError:
            pass

        print(f"{date:<13} {str(temp):<12} {conditions.title()}")

    print("-" * 65)


def main():
    print("=" * 42)
    print("       WEATHER APP")
    print("=" * 42)

    if not API_KEY:
        print("API key missing. Add OPENWEATHER_KEY to your .env file.")
        return

    while True:
        city = input("\nEnter a city (or press Enter to exit): ").strip()

        if not city:
            print("Thank you for using the Weather App!")
            break

        current = get_current_weather(city)

        if current:
            display_weather(current)

            # Use the city name returned by the API.
            actual_city = current.get("name", city)
            forecast = get_forecast(actual_city)

            if forecast:
                display_forecast(forecast)


if __name__ == "__main__":
    main()
