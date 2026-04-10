import requests
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# ML
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

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
# 🏙️ URBAN + HEALTH
# ==============================

def get_urban_factor(city):
    metro = ["Delhi","Mumbai","Kolkata"]
    return 1.3 if city in metro else 1.1

def get_health_score(city):
    metro = ["Delhi","Mumbai","Kolkata"]
    return 0.8 if city in metro else 0.5

# ==============================
# 🌫️ AQI
# ==============================

def get_aqi_label(aqi):
    return ["Unknown","Good","Fair","Moderate","Poor","Very Poor"][aqi] if aqi <=5 else "Unknown"

def fetch_aqi(lat, lon):
    try:
        res = requests.get(AQI_URL, params={"lat": lat, "lon": lon, "appid": API_KEY}, timeout=10)
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
        urban = get_urban_factor(city)
        health = get_health_score(city)
        aqi = fetch_aqi(lat, lon)

        return {
            "City": city,
            "Temperature": temp,
            "Humidity": humidity,
            "Heat_Index": heat_index,
            "Urban_Factor": urban,
            "AQI": aqi,
            "AQI_Category": get_aqi_label(aqi),
            "Health_Score": health,
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
# 🎯 FEATURE ENGINEERING
# ==============================

df["Adjusted_Heat"] = df["Heat_Index"] * df["Urban_Factor"]

df["Risk_Score"] = (
    0.4 * df["Adjusted_Heat"] +
    0.2 * df["AQI"] +
    0.2 * (df["Density"] / 10000) -
    0.2 * df["Health_Score"]
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
# 📊 ANALYSIS
# ==============================

print("\n📊 Summary:\n", df.describe())

# ==============================
# 🤖 MACHINE LEARNING
# ==============================

print("\n🤖 Training ML Model...\n")

features = [
    "Temperature","Humidity","Heat_Index",
    "Urban_Factor","AQI","Density","Health_Score"
]

X = df[features]
y = df["Risk_Level"].map({"Low": 0, "Medium": 1, "High": 2})

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("📊 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📋 Report:\n", classification_report(y_test, y_pred))

# ==============================
# 📊 VISUALIZATION
# ==============================

print("\n📊 Visualization...\n")

# Bar Chart
plt.figure(figsize=(8,5))
plt.bar(df["City"], df["Risk_Score"], color="orange")
plt.title("City vs Heatwave Risk Score")
plt.xticks(rotation=45)
plt.show()

# Heatmap
plt.figure(figsize=(8,6))
corr = df[[
    "Temperature","Humidity","Heat_Index",
    "AQI","Density","Health_Score","Risk_Score"
]].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Risk Distribution
plt.figure(figsize=(6,4))
df["Risk_Level"].value_counts().plot(
    kind="bar",
    color=["green","yellow","red"]
)
plt.title("Risk Level Distribution")
plt.show()

# ==============================
# 🗺️ MAP VISUALIZATION
# ==============================

plt.figure(figsize=(8,6))
plt.scatter(
    df["Longitude"],
    df["Latitude"],
    c=df["Risk_Score"],
    cmap="hot",
    s=200
)

plt.colorbar(label="Risk Score")
plt.title("Heatwave Risk Map (India Cities)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

for i, city in enumerate(df["City"]):
    plt.text(df["Longitude"][i], df["Latitude"][i], city)

plt.show()

# ==============================
# 📊 FEATURE IMPORTANCE
# ==============================

importances = model.feature_importances_

plt.figure(figsize=(8,5))
plt.barh(features, importances, color="purple")
plt.title("Feature Importance")
plt.show()
