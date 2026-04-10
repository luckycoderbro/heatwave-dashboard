import streamlit as st
import requests

# ==============================
# CONFIG
# ==============================
API_KEY = "d22989cb56cb3df66e315574b01cd7c1"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# ==============================
# PAGE SETTINGS
# ==============================
st.set_page_config(
    page_title="Heatwave Risk Monitor",
    layout="wide"
)

# ==============================
# CUSTOM CSS (PRO LOOK)
# ==============================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1 {
    text-align: center;
    color: #ffffff;
}
.subtitle {
    text-align: center;
    color: #bbbbbb;
    margin-bottom: 30px;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
.metric {
    font-size: 28px;
    font-weight: bold;
    color: #4CAF50;
}
.label {
    font-size: 14px;
    color: #aaaaaa;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("<h1>Heatwave Risk Monitoring System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-time environmental risk analysis</p>", unsafe_allow_html=True)

# ==============================
# INPUT SECTION
# ==============================
col1, col2 = st.columns([3,1])

with col1:
    city = st.text_input("Enter City Name", "Mumbai")

with col2:
    check = st.button("Analyze")

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

def fetch_data(city):
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

        density = 10000

        risk_score = (
            0.5 * heat_index +
            0.3 * aqi +
            0.2 * (density / 10000)
        )

        if risk_score < 30:
            risk = "Low"
            color = "#4CAF50"
        elif risk_score < 50:
            risk = "Medium"
            color = "#FFC107"
        else:
            risk = "High"
            color = "#F44336"

        return temp, humidity, aqi, risk_score, risk, color

    except:
        return None

# ==============================
# DISPLAY RESULTS
# ==============================
if check:
    result = fetch_data(city)

    if result:
        temp, humidity, aqi, risk_score, risk, color = result

        # METRIC CARDS
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="card">
            <div class="label">Temperature</div>
            <div class="metric">{temp} °C</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
            <div class="label">Humidity</div>
            <div class="metric">{humidity} %</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
            <div class="label">AQI</div>
            <div class="metric">{aqi}</div>
        </div>
        """, unsafe_allow_html=True)

        # RISK SECTION
        st.markdown("### Risk Analysis")

        st.markdown(f"""
        <div class="card">
            <div class="label">Risk Score</div>
            <div class="metric">{round(risk_score,2)}</div>
            <div class="label" style="margin-top:10px;">Risk Level</div>
            <div style="font-size:22px; color:{color}; font-weight:bold;">
                {risk}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("Unable to fetch data. Please check the city name or API key.")
