import requests
import pandas as pd
import time

print("🚀 MASTER SCRIPT STARTED...\n")

# ==============================
# 🔑 CONFIG
# ==============================

API_KEY = "d22989cb56cb3df66e315574b01cd7c1"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# WAQI TOKEN
WAQI_TOKEN = "cdbcc340bb91a5859bf0b18c5986deb0f63f0679"

LOCATIONS = [
    "Amaravati","Itanagar","Dispur","Patna","Raipur","Panaji",
    "Gandhinagar","Chandigarh","Shimla","Ranchi","Bengaluru",
    "Thiruvananthapuram","Bhopal","Mumbai","Imphal","Shillong",
    "Aizawl","Kohima","Bhubaneswar","Chandigarh","Jaipur",
    "Gangtok","Chennai","Hyderabad","Agartala","Lucknow",
    "Dehradun","Kolkata",
    "Delhi","Port Blair","Daman","Silvassa","Srinagar",
    "Leh","Kavaratti","Puducherry"
]

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
# 🌫️ AQI FUNCTION (FIXED)
# ==============================

def fetch_aqi(city):
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if data["status"] == "ok":
            aqi = data["data"]["aqi"]

            # Ensure numeric value
            if isinstance(aqi, (int, float)):
                return aqi
            else:
                return 0
        else:
            print(f"⚠️ No AQI data for {city}")
            return 0

    except Exception as e:
        print("AQI Error:", e)
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

        # ✅ NEW AQI CALL
        aqi = fetch_aqi(city)

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
    time.sleep(1)

df_weather = pd.DataFrame(records)

# ==============================
# 🔥 FIX AQI DATA TYPE (CRITICAL)
# ==============================

df_weather["AQI"] = pd.to_numeric(df_weather["AQI"], errors="coerce")
df_weather["AQI"] = df_weather["AQI"].fillna(0)

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

