import streamlit as st


import requests
import ast
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

# pip install streamlit-pandas-profiling
from streamlit.web.server.websocket_headers import _get_websocket_headers


with st.sidebar: 
    # st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Profiling Any Dataset"])
    st.info("This project application helps you build and explore your data.")


if choice == "Profiling Any Dataset": 
    st.title("Exploratory Data Analysis")
    st.title("Upload Your Dataset")
    file = st.file_uploader("Upload Your Dataset")
    if file: 
        df = pd.read_csv(file, index_col=None)
      #  df.to_csv('dataset.csv', index=None)
        st.dataframe(df)
    profile_df = df.profile_report()
    st_profile_report(profile_df)