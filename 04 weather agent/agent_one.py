from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return "City not found"

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    if "current_weather" in weather_response:
        temp = weather_response["current_weather"]["temperature"]
        wind = weather_response["current_weather"]["windspeed"]
        return f"The weather in {city} is {temp}°C with wind speed {wind} km/h"

    return "Something went wrong"


def main():
    user_query = input("> ").lower()

    if "weather" in user_query:
        city = user_query.split("in")[-1].replace("?", "").strip()
        print("🤖 :", get_weather(city))
        return

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_query}],
        max_tokens=1000
    )

    print("🤖 :", response.choices[0].message.content)


main()