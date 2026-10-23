# Python-internship-project-5

# Weather App with Live OpenWeather API

## Description
A Python command-line application that retrieves current weather
and a five-day forecast using the OpenWeather API.

## Features
- Current temperature in Celsius
- Humidity, weather description, and wind speed
- Five-day forecast
- Handles unknown cities and network/API errors
- Five-minute cache for current weather
- API key stored securely in a local .env file

## Requirements
- Python 3
- OpenWeather API key

## Installation
Install dependencies:

    python -m pip install -r requirements.txt

Create a .env file in the project folder:

    OPENWEATHER_KEY=your_actual_api_key

Replace the example value with your own key. Do not upload .env.

## Run

    python project5.py

## Security
The API key is loaded from .env using python-dotenv.
The .env file is excluded through .gitignore and must not be
committed to the public repository.
