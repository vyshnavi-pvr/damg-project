import streamlit as st 
import requests
import ast


# interact with FastAPI endpoint


import streamlit as st 
import requests
import ast


# interact with FastAPI endpoint


with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Home Page"])
    st.info("This project application helps you build and explore your data.")


if choice == "Home Page":
	username = st.text_input("Username")
	password = st.text_input("password")

	
	
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
		headers = {'accept': 'application/json',}
		data = {'grant_type': '','username': '{user_val}'.format(user_val=username),'password': '{pass_val}'.format(pass_val=password),'scope': '','client_id': '' ,'client_secret': '',}
		response = requests.post('http://127.0.0.1:8000/token', headers=headers, data=data)
		string_response = response.content.decode("utf-8") 
		dict_response = ast.literal_eval(string_response)
		auth_token = dict_response['access_token']		
		headers = {'accept': 'application/json','Authorization': 'Bearer {access_token}'.format(access_token=auth_token),}		


		# response_model = requests.get('http://127.0.0.1:8000/users/me/predict/{predict_value}'.format(predict_value=value), headers=headers)
		response_model = requests.post('http://127.0.0.1:8000/predict', json=creditCardData, headers=headers)
		string_rm = response_model.content.decode("utf-8")
		dict_rm = ast.literal_eval(string_rm)
		print(dict_rm['predictions'])
		st.success(dict_rm['predictions'])

		
		
# def predict_flashes(pixels):
#     inputs = pixels.split(',')
#     y_values= array([inputs]).reshape(-1,1)
#     prediction = reg_model.predict(y_values)
#     print(prediction)
#     return list(prediction)


# if choice == "Profiling Any Dataset": 
#     st.title("Exploratory Data Analysis")
#     st.title("Upload Your Dataset")
#     file = st.file_uploader("Upload Your Dataset")
#     if file: 
#         df = pd.read_csv(file, index_col=None)
#       #  df.to_csv('dataset.csv', index=None)
#         st.dataframe(df)
#     profile_df = df.profile_report()
#     st_profile_report(profile_df)


# if choice == "Model Performance":  
#     if st.button("See Model Performance"):
#         image = Image.open('slr1.png')
#         st.image(image, caption='Sunrise by the mountains')

