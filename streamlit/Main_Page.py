# import json
# from pathlib import Path
import streamlit as st 
import requests
import ast
from streamlit.web.server.websocket_headers import _get_websocket_headers
from streamlit.source_util import _on_pages_changed, get_pages

DEFAULT_PAGE = "Main_Page.py"


def main_page():
	st.image('https://streb.org/wp-content/themes/ken/images/woocommerce/icons/credit-cards/discover.svg')

	st.caption("Procrastination is like a credit card: It's a lot of fun until you get the bill")

	html_temp = """
	<div style="background-color:white;padding:10px">
	<h2 style="color:tomato;text-align:center;">Identifying Potential Fraud </h2>
	</div>
	"""
	st.title("LogIn")

	st.markdown(html_temp,unsafe_allow_html=True)

	username = st.text_input("Username")
	password = st.text_input("password", type="password")


	if st.button("Submit"):
		headers = {'accept': 'application/json',}
		data = {'grant_type': '','username': '{user_val}'.format(user_val=username),'password': '{pass_val}'.format(pass_val=password),'scope': '','client_id': '' ,'client_secret': '',}
		response = requests.post("http://api:8001/token", headers=headers, data=data)
		# response = requests.post('http://127.0.0.1:8000/token', headers=headers, data=data)
		string_response = response.content.decode("utf-8") 

		dict_response = ast.literal_eval(string_response)

		try:
			auth_token = dict_response['access_token']	
			json_response = response.json()
			
			st.session_state['access_token'] = json_response["access_token"]
			st.session_state['token_type'] = json_response["token_type"]
			headers = {'accept': 'application/json','Authorization': 'Bearer {access_token}'.format(access_token=auth_token),}	

			st.session_state['loggedin']='True'
		
			st.success("Loggedin")
		except KeyError:
			st.error(" Please enter correct Username or password")
		
main_page()
			
