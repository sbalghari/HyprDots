#!/usr/bin/env python3

import requests
import json
import sys

# WeatherAPI.com settings
from WeatherAPI import API_KEY, LATITUDE, LONGITUDE 

# Map WeatherAPI.com condition codes to Nerd Fonts icons
ICONS = {
    1000: "󰖨",  # Sunny
    1003: "󰖕",  # Partly cloudy
    1006: "󰖐",  # Cloudy
    1009: "󰖑",  # Overcast
    1030: "󰖑",  # Mist
    1063: "󰼳",  # Patchy rain possible
    1066: "󰼴",  # Patchy snow possible
    1069: "󰙿",  # Patchy sleet possible
    1072: "󰙿",  # Patchy freezing drizzle possible
    1087: "󰙾",  # Thundery outbreaks possible
    1114: "󰼶",  # Blowing snow
    1117: "󰼶",  # Blizzard
    1135: "󰖑",  # Fog
    1147: "󰖑",  # Freezing fog
    1150: "󰖗",  # Patchy light drizzle
    1153: "󰖗",  # Light drizzle
    1168: "󰖗",  # Freezing drizzle
    1171: "󰖗",  # Heavy freezing drizzle
    1180: "󰖗",  # Patchy light rain
    1183: "󰖗",  # Light rain
    1186: "󰖗",  # Moderate rain at times
    1189: "󰖗",  # Moderate rain
    1192: "󰖗",  # Heavy rain at times
    1195: "󰖗",  # Heavy rain
    1198: "󰖗",  # Light freezing rain
    1201: "󰖗",  # Moderate or heavy freezing rain
    1204: "󰙿",  # Light sleet
    1207: "󰙿",  # Moderate or heavy sleet
    1210: "󰼶",  # Patchy light snow
    1213: "󰼶",  # Light snow
    1216: "󰼶",  # Moderate snow
    1219: "󰼶",  # Heavy snow
    1222: "󰙿",  # Ice pellets
    1225: "󰙿",  # Light ice pellets
    1237: "󰙿",  # Moderate or heavy ice pellets
    1240: "󰖗",  # Light rain shower
    1243: "󰖗",  # Moderate or heavy rain shower
    1246: "󰖗",  # Torrential rain shower
    1249: "󰙿",  # Light sleet showers
    1252: "󰙿",  # Moderate or heavy sleet showers
    1255: "󰼶",  # Light snow showers
    1258: "󰼶",  # Moderate or heavy snow showers
    1261: "󰙿",  # Light showers of ice pellets
    1264: "󰙿",  # Moderate or heavy showers of ice pellets
    1273: "󰙾",  # Patchy light rain with thunder
    1276: "󰙾",  # Moderate or heavy rain with thunder
    1279: "󰙾",  # Patchy light snow with thunder
    1282: "󰙾",  # Moderate or heavy snow with thunder
}

# Fetch weather data from WeatherAPI.com
def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LATITUDE},{LONGITUDE}"
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

    current_weather = data.get("current", {})
    temperature = current_weather.get("temp_c", "N/A")
    condition = current_weather.get("condition", {})
    condition_code = condition.get("code", 1000)  # Default to Sunny if code is missing
    condition_text = condition.get("text", "Unknown")
    condition_text = condition_text[:20] + "..." if len(condition_text) > 20 else condition_text # Shorten the condition text
    
    # Round the temperature to the nearest integer
    if isinstance(temperature, (int, float)):
        temperature = int(round(temperature))

    # Get the icon based on the condition code
    icon = ICONS.get(condition_code, "󰖨")  # Default to Sunny if code is unknown

    return f"{icon} {condition_text}, {temperature}°C"

def main():
    weather_data = get_weather()
    output = format_weather(weather_data)
    
    # Prepare tooltip with more detailed information
    tooltip = "Weather information"
    if weather_data:
        location = weather_data.get("location", {})
        location_name = location.get("name", "Unknown")
        location_region = location.get("region", "Unknown")
        location_country = location.get("country", "Unknown")
        location_line = f"Location: {location_name}, {location_region} - {location_country}"

        current_weather = weather_data.get("current", {})
        tooltip = f"{location_line}\n"
        tooltip += f"Temperature: {current_weather.get('temp_c', 'N/A')}°C\n"
        tooltip += f"Condition: {current_weather.get('condition', {}).get('text', 'N/A')}\n"
        tooltip += f"Wind Speed: {current_weather.get('wind_kph', 'N/A')} km/h\n"
        tooltip += f"Wind Direction: {current_weather.get('wind_degree', 'N/A')}°\n"
        tooltip += f"Humidity: {current_weather.get('humidity', 'N/A')}%"
    
    print(json.dumps({"text": output, "tooltip": tooltip}))

if __name__ == "__main__":
    main()