
def calculate_biogas(df):
    total_waste = df["Forecasted Waste"].sum()
    biogas_m3 = total_waste * 0.03  # 30L of biogas per kg waste
    electricity_kwh = biogas_m3 * 1.8  # 1.8 kWh per m³ biogas
    return {"biogas_m3": biogas_m3, "electricity_kwh": electricity_kwh}
