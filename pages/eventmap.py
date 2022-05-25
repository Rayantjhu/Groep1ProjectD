import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
from datetime import datetime
import utils.database as database
from utils.settings import read_settings

def create_eventmap():
    from streamlit_autorefresh import st_autorefresh

    # Reads the settings 
    settings = read_settings()
    seconds = settings["pages"]["refresh_rate_in_seconds"]

    st_autorefresh(interval=seconds * 1000, key="map_refresh")
    st.header("Eventmap")

    # counter = seconds
    # timer = st.empty()
    # timer.write(f"Refreshing in {counter} sec")
    
    # Expander to hide the filter options if the user does not want to use them
    with st.expander("Filter options"):

         # Create the select box to pick the sound type
        option_sound_type = st.selectbox("Select sound type", ["All", "Car", "Gun", "Animal"])

        # Create the slider to pick a value for probability (between 0 and 100 with steps of 1)
        probability_slider = st.slider(label = 'Probability', value = 0, min_value = 0, max_value = 100, step = 1)

        date_cols = st.columns(2)
        
        with date_cols[0]:
            # Create the date
            start = st.date_input('Start', value = datetime.today().date())

        with date_cols[1]:
            # add a year to start date
            end = st.date_input('End', value = pd.to_datetime(start + pd.Timedelta(days=365)))

        # convert date to unix timestamp
        start_to_unix_timestamp = int(datetime.timestamp(datetime.strptime(str(start), '%Y-%m-%d')))
        end_to_unix_timestamp = int(datetime.timestamp(datetime.strptime(str(end), '%Y-%m-%d')))

    # Loads the longitude and latitude for positioning of the event map from the settings 
    latitude = settings["eventmap"]["start_latitude"]
    longitude = settings["eventmap"]["start_longitude"]

    # Draw the map
    m = leafmap.Map(
        search_control=False,
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        location=[latitude, longitude],
        zoom_start=6, key="map_refresh")

    m.add_basemap("Stamen.Terrain")

    # Get the data from excel sheet (update to DB later)
    #df = pd.read_excel("./prototype/eventmapdata.xlsx")

    # Create a database connection.
    conn = database.get_connection()

    df = pd.read_sql("SELECT * FROM event", conn)

    # Sound type filter
    if option_sound_type != "All":
        df = df[df["sound_type"] == option_sound_type.lower()] 

    # Filter probability
    df = df[df["probability"] >= probability_slider] 
    
    # Date filter
    df = df[(df["time"] >= start_to_unix_timestamp) & (df["time"] <= end_to_unix_timestamp)]

    # Add markers to the map.
    m.add_circle_markers_from_xy(
    df, x="longitude", y="latitude", radius=10, color="blue", fill_color="black")
    m.to_streamlit(width=700, height=500)


    with st.form(key="dont_refresh", clear_on_submit=False):
        event_to_download = st.number_input("Enter event ID", value=1)
        submitted = st.form_submit_button("Create download link")
        
        if submitted:
            import streamlit.components.v1 as component
            component.iframe(f"http://localhost:8501?event={event_to_download}", width=200, height=500, scrolling=False)

        # st.markdown(f"<iframe src='http://localhost:8501?event={event_to_download}'> </iframe>",unsafe_allow_html=True)
        
    # import time 
    # while counter != 0:
    #     time.sleep(1)
    #     counter -= 1
    #     timer.write(f"Refreshing in {counter} sec")
    