import streamlit as st

st.set_page_config(page_title="SkyOracle AI", layout="wide")

# -------- STYLE --------
st.markdown("""
<style>
.title { font-size:50px; font-weight:bold; color:#00ADB5; }
.subtitle { font-size:20px; color:gray; }
</style>
""", unsafe_allow_html=True)

# -------- HERO --------
st.markdown('<p class="title">🌍 SkyOracle AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predicting the sky with intelligence</p>', unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1501630834273-4b5604d2ee31", use_container_width=True)

st.write("")

st.subheader("🚀 Features")

col1, col2, col3 = st.columns(3)
col1.write("📊 Real-time analytics")
col2.write("🔮 AI predictions")
col3.write("🌍 Multi-city weather")

st.write("")

if st.button("🌤 Open Weather Dashboard"):
    st.switch_page("dashboard/app.py")