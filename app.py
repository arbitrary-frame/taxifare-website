import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# '''
# # TaxiFareModel front
# '''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

st.header("🚕 Ride Details")

# Date and time
st.subheader("📅 Date and Time of Ride")

pickup_datetime = st.text_input(
    "Enter pickup datetime (format: YYYY-MM-DD HH:MM:SS)",
    placeholder="2025-08-29 14:30:00",
    value='2014-07-06 19:18:00'
)

st.markdown("---")

# # Pickup details
# st.subheader("📍 Pickup Location")
# col1, col2 = st.columns(2)
# with col1:
#     pickup_long = st.text_input("Longitude", key=1)
# with col2:
#     pickup_lat = st.text_input("Latitude", key=2)

# # Dropoff details
# st.subheader("📍 Dropoff Location")
# col3, col4 = st.columns(2)
# with col3:
#     drop_long = st.text_input("Longitude", key=3)
# with col4:
#     drop_lat = st.text_input("Latitude", key=4)

# st.markdown("---")


# Location input method selection
# Initialize session state for coordinates if not exists
if 'pickup_lat' not in st.session_state:
    st.session_state.pickup_lat = ""
if 'pickup_long' not in st.session_state:
    st.session_state.pickup_long = ""
if 'dropoff_lat' not in st.session_state:
    st.session_state.dropoff_lat = ""
if 'dropoff_long' not in st.session_state:
    st.session_state.dropoff_long = ""

st.subheader("📍 Location Input Method")
input_method = st.radio(
    "Choose how to enter locations:",
    ["Text Input", "Map Selection"],
    horizontal=True
)

if input_method == "Text Input":
    # Original text input method
    st.subheader("📍 Pickup Location")
    col1, col2 = st.columns(2)
    with col1:
        pickup_long = st.text_input("Longitude", key="pickup_long_text",
                                  value=st.session_state.pickup_long)
    with col2:
        pickup_lat = st.text_input("Latitude", key="pickup_lat_text",
                                 value=st.session_state.pickup_lat)

    # Update session state
    st.session_state.pickup_long = pickup_long
    st.session_state.pickup_lat = pickup_lat

    st.subheader("📍 Dropoff Location")
    col3, col4 = st.columns(2)
    with col3:
        dropoff_long = st.text_input("Longitude", key="dropoff_long_text",
                                   value=st.session_state.dropoff_long)
    with col4:
        dropoff_lat = st.text_input("Latitude", key="dropoff_lat_text",
                                  value=st.session_state.dropoff_lat)

    # Update session state
    st.session_state.dropoff_long = dropoff_long
    st.session_state.dropoff_lat = dropoff_lat

else:
    # Map selection method
    st.subheader("📍 Select Locations on Map")
    st.write("Click on the map to set pickup (green) and dropoff (red) locations. Click 'Set Pickup' or 'Set Dropoff' buttons first to choose which location you're setting.")

    # Location setting mode
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        set_pickup = st.button("🟢 Set Pickup Location", use_container_width=True)
    with col_mode2:
        set_dropoff = st.button("🔴 Set Dropoff Location", use_container_width=True)

    # Initialize mode in session state
    if 'location_mode' not in st.session_state:
        st.session_state.location_mode = None

    if set_pickup:
        st.session_state.location_mode = "pickup"
    elif set_dropoff:
        st.session_state.location_mode = "dropoff"

    # Show current mode
    if st.session_state.location_mode:
        st.info(f"Click on the map to set {st.session_state.location_mode} location")

    # Create map centered on NYC (you can change this to your preferred location)
    center_lat, center_lon = 40.7128, -74.0060  # NYC coordinates
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add existing markers if coordinates are available
    if st.session_state.pickup_lat and st.session_state.pickup_long:
        try:
            pickup_lat_float = float(st.session_state.pickup_lat)
            pickup_long_float = float(st.session_state.pickup_long)
            folium.Marker(
                [pickup_lat_float, pickup_long_float],
                popup="Pickup Location",
                icon=folium.Icon(color='green', icon='play')
            ).add_to(m)
        except ValueError:
            pass

    if st.session_state.dropoff_lat and st.session_state.dropoff_long:
        try:
            dropoff_lat_float = float(st.session_state.dropoff_lat)
            dropoff_long_float = float(st.session_state.dropoff_long)
            folium.Marker(
                [dropoff_lat_float, dropoff_long_float],
                popup="Dropoff Location",
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(m)
        except ValueError:
            pass

    # Display map and capture clicks
    map_data = st_folium(m, width=700, height=500)

    # Handle map clicks
    if map_data['last_clicked'] is not None and st.session_state.location_mode is not None:
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lng = map_data['last_clicked']['lng']

        if st.session_state.location_mode == "pickup":
            st.session_state.pickup_lat = str(clicked_lat)
            st.session_state.pickup_long = str(clicked_lng)
            st.success(f"Pickup location set to: {clicked_lat:.6f}, {clicked_lng:.6f}")
        elif st.session_state.location_mode == "dropoff":
            st.session_state.dropoff_lat = str(clicked_lat)
            st.session_state.dropoff_long = str(clicked_lng)
            st.success(f"Dropoff location set to: {clicked_lat:.6f}, {clicked_lng:.6f}")

    # Display current coordinates
    col_display1, col_display2 = st.columns(2)
    with col_display1:
        st.write("**Pickup Coordinates:**")
        if st.session_state.pickup_lat and st.session_state.pickup_long:
            st.write(f"Lat: {st.session_state.pickup_lat}")
            st.write(f"Long: {st.session_state.pickup_long}")
        else:
            st.write("Not set")

    with col_display2:
        st.write("**Dropoff Coordinates:**")
        if st.session_state.dropoff_lat and st.session_state.dropoff_long:
            st.write(f"Lat: {st.session_state.dropoff_lat}")
            st.write(f"Long: {st.session_state.dropoff_long}")
        else:
            st.write("Not set")

    # Use session state values for API call
    pickup_lat = st.session_state.pickup_lat
    pickup_long = st.session_state.pickup_long
    dropoff_lat = st.session_state.dropoff_lat
    dropoff_long = st.session_state.dropoff_long


# Passenger details
st.subheader("👥 Number of passengers")
pass_count = st.selectbox("Number of passengers in the ride", list(range(1, 8)))


# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''



# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''


# set url
url = 'https://taxifare-490473674768.europe-west1.run.app/predict'

# define parameters for call
params = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': pickup_long,
    'pickup_latitude': pickup_lat,
    'dropoff_longitude': dropoff_long,
    'dropoff_latitude': dropoff_lat,
    'passenger_count': pass_count
}

response = requests.get(url,params=params)

st.markdown("---")
st.subheader("🔮 Predicted Fare")
st.text(f"${round(response.json().get("fare"),2)}")
