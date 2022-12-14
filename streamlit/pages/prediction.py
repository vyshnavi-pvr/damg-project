import streamlit as st


import requests
import ast

from streamlit.web.server.websocket_headers import _get_websocket_headers

# interact with FastAPI endpoint


with st.sidebar: 
    # st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Prediction Page"])
    st.info("This project application helps you build and explore your data.")


if choice == "Prediction Page":
	
	

	dfromh=st.text_input("Distance from home")	
	dfromlt=st.text_input("Distance from last transaction")
	rmpp=st.text_input("ratio_to_median_purchase_price")
	rr=st.text_input("repeat_retailer")
	uc=st.text_input("used_chip")
	upn=st.text_input("used_pin_number")
	oo=st.text_input("online_order")
	


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
    print(st.session_state['access_token'])

    if st.session_state['access_token'] != '':  
        access_token=st.session_state['access_token']
        headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}",
    }
        print(headers,"Printed headers")   
        # response_model = requests.get('http://127.0.0.1:8000/users/me/predict/{predict_value}'.format(predict_value=value), headers=headers)
        response_model = requests.post('http://127.0.0.1:8000/predict', json=creditCardData, headers=headers)
        string_rm = response_model.content.decode("utf-8")
        print("Printing response tree",string_rm)
        dict_rm = ast.literal_eval(string_rm)
        print(dict_rm['predictions'])
        st.success(dict_rm['predictions'])
        print("response model",response_model)
    else:
        print("No access token")
            

