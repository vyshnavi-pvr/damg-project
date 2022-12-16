import streamlit as st


import requests
import ast
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report


from streamlit.web.server.websocket_headers import _get_websocket_headers


with st.sidebar: 
    st.title("Analysis of data")
    st.info("This page can help you check all kinds of statistics and analysis in the given dataset")


st.title("Exploratory Data Analysis")
st.title("Upload Your Dataset")
file = st.file_uploader("Upload Your Dataset")
if st.button("Submit"):
    if file: 
        df = pd.read_csv(file, index_col=None)
        st.dataframe(df)
    profile_df = df.profile_report()
    st_profile_report(profile_df)
