import os
import pandas as pd
import plotly.express as px
from prophet import Prophet
from datetime import datetime, date
import streamlit as st

# --------------------------
# 1. Page Configuration
# --------------------------
st.set_page_config(page_title="Biogas Forecasting Dashboard", layout="wide")
st.title("♻️ Smart Dashboard for Food Waste Forecasting & Biogas Conversion Planning")
st.markdown("This dashboard visualizes categorized food waste and forecasts biogas production.")

# --------------------------
# 2. Load Main Dataset
# --------------------------
try:
    df = pd.read_csv("categorized_food_waste_dataset.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # --------------------------
    # 3. Tabs
    # --------------------------
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "📈 Forecasting", "📋 Raw Data", "➕ Add Daily Waste"])

    # ---- Tab 1: Data Overview ----
    with tab1:
        st.subheader("Total Biogas Production Over Time")
        fig_total = px.line(df, x='Date', y='Total_Biogas_m3', title='Daily Biogas Production (m³)')
        st.plotly_chart(fig_total, use_container_width=True)

        st.subheader("Food Category Wise Waste Input (kg)")
        fig_cat = px.area(
            df,
            x="Date",
            y=["Vegetable_Waste_kg", "Rice_Waste_kg", "Dairy_Waste_kg", "Meat_Waste_kg"],
            title="Food Waste by Category (kg)",
            labels={"value": "Waste (kg)", "variable": "Category"}
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # ---- Tab 2: Forecasting ----
    with tab2:
        st.subheader("Forecast Biogas Production (Next 30 Days)")
        prophet_df = df[['Date', 'Total_Biogas_m3']].rename(columns={'Date': 'ds', 'Total_Biogas_m3': 'y'})

        model = Prophet()
        model.fit(prophet_df)

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        fig_forecast = px.line(forecast, x='ds', y='yhat', title='Biogas Forecast (m³)')
        st.plotly_chart(fig_forecast, use_container_width=True)

    # ---- Tab 3: Raw Data ----
    with tab3:
        st.subheader("Raw Dataset from Daily Logs")

        log_file = "daily_food_waste_log.csv"
        if os.path.exists(log_file):
            raw_data = pd.read_csv(log_file)
            raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], errors='coerce')
            raw_data = raw_data.sort_values(by='Timestamp', ascending=False)
            st.dataframe(raw_data, use_container_width=True)
        else:
            st.info("No log file found yet. Add entries to generate one.")

# ---- Tab 4: Add Daily Entry ----
    with tab4:
        st.subheader("📅 Log Today's Food Waste")
        current_time = datetime.now()

        st.write(f"🕒 **Current Time:** {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        with st.form("food_waste_form", clear_on_submit=True):
            food_type = st.selectbox("Food Category", ["Vegetables", "Fruits", "Rice", "Meat", "Dairy", "Other"])
            quantity = st.number_input("Quantity (in kg)", min_value=0.0, format="%.2f")
            submitted = st.form_submit_button("Add Entry")

            if submitted:
                timestamp = datetime.now()
                new_entry = pd.DataFrame([[timestamp, food_type, quantity]],
                                         columns=["Timestamp", "Food_Category", "Quantity_kg"])

                if os.path.exists(log_file):
                    existing_data = pd.read_csv(log_file)
                    updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
                else:
                    updated_data = new_entry

                try:
                    updated_data.to_csv(log_file, index=False)
                    st.success(f"✅ Entry added: {quantity} kg of {food_type} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.rerun()  # 🔄 Instantly reload the app
                except PermissionError:
                    st.error("❌ Permission denied while writing to the log file. Please close it if open.")

except FileNotFoundError:
    st.error("❌ categorized_food_waste_dataset.csv file not found. Please place it in the app directory.")
