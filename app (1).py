import streamlit as st
import pickle
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="wide")

# ===== CUSTOM CSS =====
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}
.main {
    background-color: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 15px;
}
h1 {
    color: #1f4037;
    text-align: center;
}
.stButton>button {
    background-color: #1f4037;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
.stButton>button:hover {
    background-color: #14532d;
}
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL =====
model = pickle.load(open('car_price_model.pkl', 'rb'))

# ===== TITLE =====
st.markdown("<h1>🚗 Car Price Prediction</h1>", unsafe_allow_html=True)
st.write("### Enter car details below 👇")

# ===== INPUT LAYOUT =====
col1, col2 = st.columns(2)

with col1:
    present_price = st.number_input("💰 Present Price (Lakhs)", 0.5, 100.0, 5.0)
    kms_driven = st.number_input("📍 Kms Driven", 0, 500000, 15000)
    owner = st.selectbox("👤 Previous Owners", [0, 1, 2, 3])

with col2:
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "CNG", "Diesel"])
    seller = st.selectbox("🏢 Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("⚙ Transmission", ["Manual", "Automatic"])
    age = st.number_input("📅 Car Age (Years)", 0, 30, 5)

# ===== ENCODING =====
fuel_diesel = 1 if fuel == "Diesel" else 0
fuel_petrol = 1 if fuel == "Petrol" else 0
seller_individual = 1 if seller == "Individual" else 0
transmission_manual = 1 if transmission == "Manual" else 0

# ===== PREDICTION =====
st.markdown("---")

col_btn, col_result = st.columns([1,2])

with col_btn:
    predict_btn = st.button("🚀 Predict Price")

with col_result:
    if predict_btn:
        features = np.array([[present_price, kms_driven, owner, age,
                              fuel_diesel, fuel_petrol,
                              seller_individual, transmission_manual]])

        prediction = model.predict(features)

        if prediction[0] < 0:
            st.error("❌ Invalid price")
        else:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #11998e, #38ef7d);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            ">
                💸 Estimated Price <br><br>
                ₹ {round(prediction[0], 2)} Lakhs
            </div>
            """, unsafe_allow_html=True)
