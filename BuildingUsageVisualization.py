#Individual Project for CSC630
#2/21/2022
#Author: Natalia Muromcew

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# PAGE LAYOUT
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")
st.title("Andover Classroom Usage")
st.write("This is a visulization of how many classes are held in each building " +
        "during each class period of the day. Use the silder to view each period " +
        "or scroll down for a photo comparison between each periods. I collected " +
        "data from the Winter Term 2022 Master Schedule and used tutorials on the " +
        "StreamLit documentation (link: https://docs.streamlit.io/)")

#Slider for Period
period_selected = st.slider("Select class period: ", 1, 7)

# Loading Data
DATE_TIME = "date/time"

@st.experimental_memo
def load_data(nrows):
    data = pd.read_csv("Book2.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data(531)

def load_data1(nrows):
    data1 = pd.read_csv("Book3.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data1.rename(lowercase, axis="columns", inplace=True)
    data1[DATE_TIME] = pd.to_datetime(data1[DATE_TIME])
    return data1

data1 = load_data1(7)

#MAP FUNCTION
def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 60,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=16,
                elevation_scale=13,
                elevation_range=[0, 10],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

data = data[data[DATE_TIME].dt.hour == period_selected]

map(data, 42.64716088236887, -71.13206225340619, 16.3)

data1 = data1[data1[DATE_TIME].dt.hour == period_selected]

st.write("Data Table")
st.table(data1)
