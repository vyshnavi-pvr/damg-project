import streamlit as st


import requests
import ast

from streamlit.web.server.websocket_headers import _get_websocket_headers

# interact with FastAPI endpoint


with st.sidebar: 
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Prediction Page"])
    st.info("This project application helps you detect whether a given transaction is fraud or not.")


if choice == "Prediction Page":

    dfromh=st.text_input("Distance from home")	
    dfromlt=st.text_input("Distance from last transaction")
    rmpp=st.text_input("ratio_to_median_purchase_price")
    options= ['0', '1']
    rr=st.selectbox("Is it a repeated retailer", ["-"] + options)
    uc=st.selectbox("Select if a credit chip card is used", ["-"] + options)
    upn=st.selectbox("Select if pin number is used", ["-"] + options)
    oo=st.selectbox("Select if it is an online_order", ["-"] + options)
    # oo=st.text_input("online_order")

    creditCardData= {
  "distance_from_home": dfromh,
  "distance_from_last_transaction": dfromlt,
  "ratio_to_median_purchase_price": rmpp,
  "repeat_retailer": rr,
  "used_chip": uc,
  "used_pin_number": upn,
  "online_order": oo
    }

    if st.button("Submit"):

        try:

            # print(st.session_state['access_token'])
            
            access_token=st.session_state['access_token']
            headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {access_token}",
        }

        except KeyError:
            st.error("Please Login with your username and password")
            # print(headers,"Printed headers")   
            # response_model = requests.post('http://api:8001/predict/random_forest', json=creditCardData, headers=headers)
        response_model = requests.post('http://127.0.0.1:8000/predict/random_forest', json=creditCardData, headers=headers)
        string_rm = response_model.content.decode("utf-8")
        # print("Printing response tree",string_rm)
        dict_rm = ast.literal_eval(string_rm)
        # print(dict_rm['predictions'])
        try:
            st.success(dict_rm['predictions'])

        except KeyError:
            st.error("Enter all the transaction details ")
            # print("response model",response_model)


        
                

