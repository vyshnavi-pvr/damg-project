import streamlit as st 
import requests
import ast

from streamlit.web.server.websocket_headers import _get_websocket_headers


# interact with FastAPI endpoint


with st.sidebar: 
    
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Home Page"])
    st.info("This project application helps you build and explore your data.")


if choice == "Home Page":
	username = st.text_input("Username")
	password = st.text_input("password", type="password")


	if st.button("Submit"):
		headers = {'accept': 'application/json',}
		data = {'grant_type': '','username': '{user_val}'.format(user_val=username),'password': '{pass_val}'.format(pass_val=password),'scope': '','client_id': '' ,'client_secret': '',}
		# response = requests.post("http://api:8001/token", headers=headers, data=data)
		response = requests.post('http://127.0.0.1:8000/token', headers=headers, data=data)
		string_response = response.content.decode("utf-8") 

		dict_response = ast.literal_eval(string_response)

		try:
			auth_token = dict_response['access_token']	
			json_response = response.json()
		
			st.session_state['access_token'] = json_response["access_token"]
			st.session_state['token_type'] = json_response["token_type"]
			headers = {'accept': 'application/json','Authorization': 'Bearer {access_token}'.format(access_token=auth_token),}	

		
			st.success("Loggedin")
		except KeyError:
			st.error(" Please enter correct Username or password")
		

		

		


	
# streamlit run app.py
# http://localhost:8501
		
