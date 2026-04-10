import requests
import pandas as pd
import time

print("🚀 MASTER SCRIPT STARTED...\n")

# ==============================
# 🔑 CONFIG
# ==============================

API_KEY = "d22989cb56cb3df66e315574b01cd7c1"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

LOCATIONS = ["Delhi", "Mumbai", "Kolkata"]

# ==============================
# 📊 POPULATION DATA
# ==============================

population_data = [
    {"City": "Delhi", "Population": 32000000, "Area_km2": 1484},
    {"City": "Mumbai", "Population": 20000000, "Area_km2": 603},
    {"City": "Kolkata", "Population": 15000000, "Area_km2": 185}
]

df_pop = pd.DataFrame(population_data)
df_pop["Density"] = df_pop["Population"] / df_pop["Area_km2"]

# ==============================
# 🌫️ AQI FUNCTION
# ==============================

def fetch_aqi(lat, lon):
    try:
        res = requests.get(AQI_URL, params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }, timeout=10)

        data = res.json()
        return data.get("list", [{}])[0].get("main", {}).get("aqi", 0)
    except:
        return 0

# ==============================
# 📡 FETCH WEATHER
# ==============================

def fetch_weather(city):
    print(f"➡️ Fetching: {city}")

    try:
        res = requests.get(WEATHER_URL, params={
            "q": f"{city},IN",
            "appid": API_KEY,
            "units": "metric"
        }, timeout=10)

        data = res.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        heat_index = temp + (0.33 * humidity) - 0.7
        aqi = fetch_aqi(lat, lon)

        return {
            "City": city,
            "Temperature": temp,
            "Humidity": humidity,
            "Heat_Index": heat_index,
            "AQI": aqi,
            "Latitude": lat,
            "Longitude": lon
        }

    except Exception as e:
        print("Error:", e)
        return None

# ==============================
# 🚀 DATA COLLECTION
# ==============================

records = []

for city in LOCATIONS:
    r = fetch_weather(city)
    if r:
        records.append(r)
    time.sleep(2)

df_weather = pd.DataFrame(records)

# ==============================
# 🔗 MERGE DATA
# ==============================

df = pd.merge(df_weather, df_pop, on="City", how="left")

print("\n✅ Data Merged!\n")

# ==============================
# 🎯 RISK CALCULATION
# ==============================

df["Risk_Score"] = (
    0.5 * df["Heat_Index"] +
    0.3 * df["AQI"] +
    0.2 * (df["Density"] / 10000)
)

def get_risk_level(score):
    if score < 30:
        return "Low"
    elif score < 50:
        return "Medium"
    else:
        return "High"

df["Risk_Level"] = df["Risk_Score"].apply(get_risk_level)

# ==============================
# 💾 SAVE DATASET
# ==============================

df.to_csv("final_heatwave_dataset.csv", index=False)

print("🔥 Dataset Saved!\n")
print(df.head())

# ==============================
# 📊 SUMMARY
# ==============================

print("\n📊 Summary:\n", df.describe())