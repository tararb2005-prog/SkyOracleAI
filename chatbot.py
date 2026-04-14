import streamlit as st

def chatbot():
    st.subheader("🤖 SkyOracle AI Assistant")

    user_input = st.text_input("Ask me about weather:")

    if user_input:
        text = user_input.lower()

        if "temperature" in text or "hot" in text:
            st.success("🌡 Temperature seems to be rising in upcoming days!")

        elif "humidity" in text:
            st.info("💧 Humidity levels are moderate.")

        elif "rain" in text:
            st.warning("🌧 There might be chances of rain.")

        elif "prediction" in text:
            st.write("🔮 Future forecast shows slight variation in temperature.")

        else:
            st.write("🤖 I'm learning! Ask about temperature, rain, or humidity.")