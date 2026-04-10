import requests
import pandas as pd
import time
from datetime import datetime

# ==============================
# CONFIG
# ==============================
API_KEY = "d22989cb56cb3df66e315574b01cd7c1"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

CITIES = ["Delhi", "Mumbai", "Kolkata"]

# ==============================
# FUNCTIONS
# ==============================
def get_aqi(lat, lon):
    try:
        res = requests.get(AQI_URL, params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        })
        return res.json()["list"][0]["main"]["aqi"]
    except:
        return 0

def fetch_city_data(city):
    try:
        res = requests.get(WEATHER_URL, params={
            "q": f"{city},IN",
            "appid": API_KEY,
            "units": "metric"
        })

        data = res.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        heat_index = temp + (0.33 * humidity) - 0.7
        aqi = get_aqi(lat, lon)

        return {
            "City": city,
            "Temperature": temp,
            "Humidity": humidity,
            "AQI": aqi,
            "Heat_Index": heat_index,
            "Timestamp": datetime.now()
        }

    except Exception as e:
        print(f"Error fetching {city}:", e)
        return None

# ==============================
# MAIN FUNCTION (IMPORTANT)
# ==============================
def collect_data():
    records = []

    for city in CITIES:
        print(f"Fetching {city}...")
        data = fetch_city_data(city)
        if data:
            records.append(data)

    if records:
        df = pd.DataFrame(records)

        # Save CSV
        file_name = "live_heatwave_data.csv"
        df.to_csv(file_name, index=False)

        print(f"✅ Data saved to {file_name}")

        return df  # 👈 IMPORTANT (returns data for further use)

    else:
        print("⚠️ No data collected")
        return None

# ==============================
# AGENT LOOP
# ==============================
def run_agent(interval=30):
    print("🚀 AI Agent Running...\n")

    while True:
        df = collect_data()

        if df is not None:
            print(df.head())  # preview

        print(f"⏳ Waiting {interval} seconds...\n")
        time.sleep(interval)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run_agent()