#!/usr/bin/env python3
import requests
import json
import sys

# Open-Meteo API settings
from location import LATITUDE, LONGITUDE
UNITS = "celsius"
TIMEZONE = "auto"

ICONS = {
    "clear": "󰖨",
    "cloudy": "",
    "rain": "",
    "snow": "",
    "thunderstorm": "",
    "fog": "",
}

# Fetch weather data from Open-Meteo
def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true&temperature_unit={UNITS}&timezone={TIMEZONE}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch weather data - {e}", file=sys.stderr)
        return None

# Format weather output for Waybar
def format_weather(data):
    if not data:
        return "⛔ Weather Unavailable"

    current_weather = data.get("current_weather", {})
    temperature = current_weather.get("temperature", "N/A")
    weather_code = current_weather.get("weathercode", 0)
    
    # Round the temperature to the nearest integer
    if isinstance(temperature, (int, float)):
        temperature = int(round(temperature))

    # Map weather codes to conditions (Open-Meteo uses WMO codes)
    weather_conditions = {
        0: "clear",
        1: "clear",
        2: "cloudy",
        3: "cloudy",
        45: "fog",
        48: "fog",
        61: "rain",
        63: "rain",
        65: "rain",
        66: "rain",
        67: "rain",
        71: "snow",
        73: "snow",
        75: "snow",
        77: "snow",
        80: "rain",
        81: "rain",
        82: "rain",
        85: "snow",
        86: "snow",
        95: "thunderstorm",
        96: "thunderstorm",
        99: "thunderstorm",
    }

    condition = weather_conditions.get(weather_code, "unknown")
    icon = ICONS.get(condition, "🌍")

    return f"{icon} {condition.capitalize()}, {temperature}°C"

def main():
    weather_data = get_weather()
    output = format_weather(weather_data)
    print(json.dumps({"text": output, "tooltip": "Weather information"}))

if __name__ == "__main__":
    main()