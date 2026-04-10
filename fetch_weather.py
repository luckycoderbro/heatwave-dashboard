import requests
import pandas as pd
import time
import datetime

# ==============================
# 🔑 CONFIGURATION
# ==============================

API_KEY = "d22989cb56cb3df66e315574b01cd7c1"

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Major cities across India
LOCATIONS = list(set([
    "Delhi","Mumbai","Kolkata","Chennai","Bengaluru","Hyderabad",
    "Chandigarh","Jaipur","Lucknow","Kanpur","Agra","Varanasi",
    "Prayagraj","Ghaziabad","Noida","Gurgaon","Faridabad",
    "Amritsar","Ludhiana","Jalandhar","Dehradun","Shimla",
    "Srinagar","Jammu",
    "Ahmedabad","Surat","Vadodara","Rajkot","Pune",
    "Nagpur","Nashik","Aurangabad","Panaji",
    "Kochi","Thiruvananthapuram","Coimbatore","Madurai",
    "Mysuru","Vijayawada","Visakhapatnam",
    "Patna","Ranchi","Bhubaneswar","Cuttack",
    "Dhanbad","Gaya",
    "Bhopal","Indore","Jabalpur","Raipur","Bilaspur",
    "Guwahati","Dispur","Shillong","Agartala",
    "Aizawl","Imphal","Itanagar","Gangtok","Kohima"
]))

# Number of cycles (increase for more data)
NUM_CYCLES = 3

# Delay settings
REQUEST_DELAY = 1   # seconds between API calls
CYCLE_DELAY = 5     # seconds between cycles

# ==============================
# 📡 FUNCTION: FETCH WEATHER DATA
# ==============================

def fetch_weather(city):
    """Fetch weather data for a given city"""
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            record = {
                "City": city,
                "Timestamp": datetime.datetime.now(),
                "Latitude": data["coord"]["lat"],
                "Longitude": data["coord"]["lon"],
                "Temperature (°C)": data["main"]["temp"],
                "Humidity (%)": data["main"]["humidity"],
                "Pressure (hPa)": data["main"]["pressure"],
                "Weather": data["weather"][0]["description"]
            }
            
            return record
        
        else:
            print(f"⚠️ API Error for {city}: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Exception for {city}: {e}")
        return None

# ==============================
# 🚀 MAIN DATA COLLECTION LOOP
# ==============================

def collect_data():
    """Collect weather data for all cities"""
    
    all_records = []
    
    print("\n🚀 Starting Data Collection...\n")
    
    for cycle in range(NUM_CYCLES):
        print(f"\n🔁 Cycle {cycle+1}/{NUM_CYCLES} started...\n")
        
        for city in LOCATIONS:
            record = fetch_weather(city)
            
            if record:
                all_records.append(record)
                print(f"✅ Data collected: {city}")
            
            time.sleep(REQUEST_DELAY)
        
        print("\n⏳ Waiting before next cycle...\n")
        time.sleep(CYCLE_DELAY)
    
    return all_records

# ==============================
# 💾 SAVE DATASET
# ==============================

def save_dataset(records):
    """Save dataset to CSV"""
    
    df = pd.DataFrame(records)
    
    filename = "india_weather_dataset.csv"
    df.to_csv(filename, index=False)
    
    print("\n🔥 DATA COLLECTION COMPLETED!")
    print(f"📁 Dataset saved as: {filename}")
    print(f"📊 Total records collected: {len(df)}\n")
    
    print(df.head())  # preview

# ==============================
# ▶️ RUN PIPELINE
# ==============================

if __name__ == "__main__":
    
    data = collect_data()
    
    if data:
        save_dataset(data)
    else:
        print("❌ No data collected!")
