import streamlit as st
import pickle
import numpy as np

# 1. Load the model you just saved in Jupyter
model = pickle.load(open('car_price_model.pkl', 'rb'))

st.set_page_config(page_title="Car Price Predictor")
st.title("🚗 Car Resale Price Predictor")
st.markdown("Enter the details below to estimate the selling price.")

# 2. Match the inputs to your X_train columns:
# [Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, Age]

col1, col2 = st.columns(2)

with col1:
    present_price = st.number_input("Present Showroom Price (In Lakhs)", 0.5, 100.0, 5.0)
    kms_driven = st.number_input("Kilometers Driven", 0, 500000, 15000)
    owner = st.selectbox("Previous Owners", [0, 1, 3])

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Are you a Dealer or Individual?", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission Type", ["Manual", "Automatic"])
    age = st.number_input("Age of the Car (Years)", 0, 30, 5)

# 3. Convert Categorical text to the numbers your model expects
fuel_diesel = 1 if fuel_type == "Diesel" else 0
fuel_petrol = 1 if fuel_type == "Petrol" else 0

seller_individual = 1 if seller_type == "Individual" else 0
transmission_manual = 1 if transmission == "Manual" else 0

# 4. Prediction Trigger
if st.button("Predict Selling Price"):
    # Create the feature array in the exact order of your training data
    features = np.array([[present_price, kms_driven, owner, age,
                      fuel_diesel, fuel_petrol,
                      seller_individual, transmission_manual]])
    
    prediction = model.predict(features)
    
    # Output the result
    if prediction[0] < 0:
        st.error("Sorry, this car cannot be sold.")
    else:
        st.success(f"Estimated Resale Value: ₹{prediction[0]:.2f} Lakhs")