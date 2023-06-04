import time
import streamlit as st
import pandas as pd
import folium
from folium import plugins, folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="Search Lat and Long by country name ",
    layout="wide",
    initial_sidebar_state="expanded",
    )

st.subheader("Countries latitude and longitude")
st.empty()


def clear_text():
    st.session_state["text"] = ""


with st.sidebar.subheader("Enter the country by name"):
    names = st.sidebar.text_input("Enter country name :", key="text")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        btn_submit = st.button("Submit")
    with col2:
        st.button("Cancel", on_click=clear_text)


def filter_by_name():
    df = pd.read_excel('Country_Dataset.xlsx')
    st.dataframe(df)
    if names is None:
        st.table(df)
    else:
        df2 = df[df["name"] == names]
        lat = df2.set_index('name').to_dict()['latitude']
        lon = df2.set_index('name').to_dict()['longitude']
        lat_val = dict_values(lat)
        lon_val = dict_values(lon)
        if len(df2) != 0:
            st.write("Searched country is " + str(names))
            st.dataframe(df2)
        return lat_val, lon_val


def dict_values(pos_val):
    for key, val in pos_val.items():
        return str(val)


lt, ln = filter_by_name()
if lt and ln is not None:
    with st.spinner('Wait for graph to load in few seconds....'):
        time.sleep(2)
        m = folium.Map(location=[lt, ln], zoom_start=5, width="%100", height="%100")
        minimap = plugins.MiniMap()
        m.add_child(minimap)
        st_data = st_folium(m, width=725)
