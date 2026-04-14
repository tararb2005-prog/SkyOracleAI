import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime
import random

st.set_page_config(page_title="SkyOracle AI", layout="wide")

API_KEY = "86e92809c77090b0ce63eb9a4b258c1e"

# ---------------- BACKGROUND ----------------
st.markdown("""
<style>
header, footer {visibility:hidden;}

.stApp {
    background:
    linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.25)),
    url("https://images.unsplash.com/photo-1499346030926-9a72daac6c63");
    background-size: cover;
    background-attachment: fixed;
}

.stButton button {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    color:white;
    border-radius:10px;
    padding:10px 25px;
    font-weight:bold;
}

.card {
    background: rgba(255,255,255,0.2);
    padding:25px;
    border-radius:20px;
    text-align:center;
    backdrop-filter: blur(10px);
}

h1,h2,h3,p {color:white !important;}
.big {font-size:70px; text-align:center;}
</style>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown("<h1 style='text-align:center;'>🌍 SkyOracle AI</h1>", unsafe_allow_html=True)
city = st.text_input("Enter City")

if "weather" not in st.session_state:
    st.session_state.weather = None
    st.session_state.forecast = None

if st.button("Get Weather") and city:
    w_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    f_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    w = requests.get(w_url).json()
    f = requests.get(f_url).json()

    if w.get("cod") != 200:
        st.error("City not found ❌")
    else:
        st.session_state.weather = w
        st.session_state.forecast = f

# ---------------- ICON FUNCTION ----------------
def get_icon(main):
    if main == "Rain":
        return "🌧️"
    elif main == "Clouds":
        return "☁️"
    elif main == "Clear":
        return "☀️"
    elif main == "Thunderstorm":
        return "⛈️"
    elif main == "Snow":
        return "❄️"
    return "🌤️"

# ---------------- DISPLAY ----------------
if st.session_state.weather:

    w = st.session_state.weather
    f = st.session_state.forecast

    temp = w["main"]["temp"]
    feels = w["main"]["feels_like"]
    humidity = w["main"]["humidity"]
    desc = w["weather"][0]["description"].title()
    main = w["weather"][0]["main"]

    st.markdown(f"<div class='big'>{temp:.0f}°</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center'>{get_icon(main)} {desc}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center'>Feels like {feels:.1f}°C</p>", unsafe_allow_html=True)

    # ---------------- HOURLY ----------------
    st.markdown("## ⏰ Hourly Forecast")
    cols = st.columns(5)

    for i in range(5):
        row = f["list"][i]
        time = datetime.fromtimestamp(row["dt"]).strftime("%I:%M %p")
        main = row["weather"][0]["main"]

        with cols[i]:
            st.markdown(f"""
            <div class="card">
            <h3>{time}</h3>
            <h1>{get_icon(main)}</h1>
            <p>{row['main']['temp']:.1f}°C</p>
            <p>{row['main']['humidity']}%</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- DAILY (REAL MIN/MAX) ----------------
    st.markdown("## 📅 5-Day Forecast")

    daily_data = {}

    for item in f["list"]:
        date = datetime.fromtimestamp(item["dt"]).strftime("%d %b")
        temp = item["main"]["temp"]
        weather = item["weather"][0]["main"]

        if date not in daily_data:
            daily_data[date] = {
                "temps": [],
                "weather": weather
            }

        daily_data[date]["temps"].append(temp)

    cols = st.columns(5)
    dates = list(daily_data.keys())[:5]

    for i, date in enumerate(dates):
        temps = daily_data[date]["temps"]
        min_temp = min(temps)
        max_temp = max(temps)
        weather = daily_data[date]["weather"]

        with cols[i]:
            st.markdown(f"""
            <div class="card">
            <h3>{date}</h3>
            <h1>{get_icon(weather)}</h1>
            <p>{max_temp:.1f}° / {min_temp:.1f}°</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- DETAILS ----------------
    st.markdown("## 🌤 Weather Details")

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        st.markdown(f"<div class='card'><h3>🌡 Feels Like</h3><h2>{feels:.1f}°C</h2></div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='card'><h3>💧 Humidity</h3><h2>{humidity}%</h2></div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='card'><h3>🌬 Wind</h3><h2>{w['wind']['speed']} m/s</h2></div>", unsafe_allow_html=True)

    with c4:
        st.markdown(f"<div class='card'><h3>🌍 Pressure</h3><h2>{w['main']['pressure']} hPa</h2></div>", unsafe_allow_html=True)

    # ---------------- MAP ----------------
    st.markdown("## 🌍 Live Weather Radar")

    lat = w["coord"]["lat"]
    lon = w["coord"]["lon"]

    m = folium.Map(location=[lat, lon], zoom_start=6)

    folium.TileLayer(
        tiles=f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="OpenWeatherMap",
        name="Rain"
    ).add_to(m)

    folium.TileLayer(
        tiles=f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
        attr="OpenWeatherMap",
        name="Clouds"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st_folium(m, width=900, height=500)

else:
    st.info("Enter city and click Get Weather")