import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    rows = []

    for i in data["list"]:
        rows.append({
            "time": i["dt_txt"],
            "temp": i["main"]["temp"],
            "humidity": i["main"]["humidity"],
            "weather": i["weather"][0]["main"]
        })

    df = pd.DataFrame(rows)
    df.to_csv("data/raw.csv", index=False)