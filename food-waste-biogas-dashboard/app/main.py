
import streamlit as st
from app.forecasting import generate_forecast
from app.conversion import calculate_biogas

st.set_page_config(page_title="Food Waste to Biogas Dashboard", layout="wide")

st.title("🍽️ Smart Dashboard for Food Waste Forecasting and Biogas Conversion")

uploaded_file = st.file_uploader("Upload daily food waste data (CSV)", type="csv")
if uploaded_file:
    forecast_df = generate_forecast(uploaded_file)
    st.subheader("📈 Forecasted Food Waste")
    st.line_chart(forecast_df["Forecasted Waste"])

    biogas_info = calculate_biogas(forecast_df)
    st.subheader("⚡ Estimated Energy Output")
    st.write(f"Biogas (m³): {biogas_info['biogas_m3']:.2f}")
    st.write(f"Electricity (kWh): {biogas_info['electricity_kwh']:.2f}")
else:
    st.info("Please upload a CSV file to get started.")
