import streamlit as st
import pickle
import json
import pandas as pd
import numpy as np
# Load the trained model
model = pickle.load(open('Real_Estate_Price_Prediction.pickle','rb'))

st.markdown(
    """
    <style>
    body {
        background-image: url('bhp_image.png');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the JSON file
with open('columns.json', 'r') as json_file:
    data = json.load(json_file)['data_columns']

# Extract the options from the "data_columns" key
Location = data[3:]

def prediction(area, bhk, bedroom, select_location):
    # Prepare the input data as a list of values in the same order as your model expects
    input_data = [area, bhk, bedroom] + [0] * len(Location)  # Initialize location values to 0
    
    # Find the index of the selected location and set its value to 1
    location_index = Location.index(select_location)
    input_data[location_index + 3] = 1
    
    # Make the prediction using the model
    predicted_price = model.predict([input_data])[0]
    
    return predicted_price

def main():
    # Set the title of the web app
    st.title("Bangalore Home Price Prediction")

    # Create input fields for Area, BHK, Bedroom, and Location
    area = st.number_input('Area (in SQFT)',min_value=50)

    bhk = st.radio("BHK", options=[1, 2, 3, 4, 5])

    bedroom = st.radio("Bathrooms", options=[1, 2, 3, 4, 5])

    select_location = st.selectbox("Location", Location)

    result = ""

    # Make a prediction when the Predict button is clicked
    if st.button("Predict"):
        result = prediction(area, bhk, bedroom, select_location)
        st.success(f"Predicted Price: ₹{result:.2f} Lakhs")

if __name__ == '__main__':
    main()
