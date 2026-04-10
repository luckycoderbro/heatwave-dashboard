from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
CITIES = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"]

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


API_KEY = "d22989cb56cb3df66e315574b01cd7c1"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

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

def fetch_data(city):
    try:
        res = requests.get(WEATHER_URL, params={
            "q": f"{city},IN",
            "appid": API_KEY,
            "units": "metric"
        })
        data = res.json()

        if str(data.get("cod", "200")) != "200":
            return {"error": data.get("message", "City not found")}

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        heat_index = temp + (0.33 * humidity) - 0.7

        aqi = get_aqi(lat, lon)

        density = 10000

        risk_score = (
            0.5 * heat_index +
            0.3 * aqi +
            0.2 * (density / 10000)
        )

        if risk_score < 30:
            risk = "Low"
        elif risk_score < 50:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "city": city,
            "lat": lat,
            "lon": lon,
            "temperature": temp,
            "humidity": humidity,
            "aqi": aqi,
            "density": density,
            "heat_index": heat_index,
            "risk_score": risk_score,
            "risk_level": risk
        }

    except Exception as e:
        return {"error": "Unable to fetch data"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-risk", methods=["GET"])
def get_risk():
    city = request.args.get("city", "")
    if not city:
        return jsonify({"error": "City not supported"})
    
    result = fetch_data(city)
    return jsonify(result)

@app.route("/get-global-data", methods=["GET"])
def get_global_data():
    results = []
    for city in CITIES:
        data = fetch_data(city)
        if "error" not in data:
            results.append(data)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
