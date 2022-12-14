import streamlit as st 
import requests
import ast
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report


# interact with FastAPI endpoint


import streamlit as st 
import requests
import ast


# interact with FastAPI endpoint


# with st.sidebar: 
#     # st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
#     st.title("UI interface for Model as a service")
#     choice = st.radio("Navigation", ["Home Page"])
#     st.info("This project application helps you build and explore your data.")
with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Home Page","Profiling Any Dataset","Manually Checking Predictions", "Statics", "Try Different Models"])
    
    st.info("This project application helps you build and explore your data.")

if choice == "Home Page":
    st.title("Basic training of a simple ML Regression model using a single feature/predictor/input")
    
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Model as a Service ML App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    if st.button("About"):
        st.text("Lets Learn")
        st.text("Built with Streamlit")


if choice == "Manually Checking Predictions":
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

###########################################################################################################
#Functions to perform in app!!
# def get_dataset(dataset_name):
# 	if dataset_name=="Heart Attack":
# 		bucket = "damg-project"
# 		file_name = "card_transdata.csv"


# 		s3 = boto3.client('s3') 
# 	# 's3' is a key word. create connection to S3 using default config and all buckets within S3

# 		obj = s3.get_object(Bucket= bucket, Key= file_name) 
# 	# get object and file (key) from bucket

# 		data = pd.read_csv(obj['Body'])
# 		st.write('Shape of the dataframe: ',initial_df.shape)

# 		#data=pd.read_csv("https://raw.githubusercontent.com/advikmaniar/ML-Healthcare-Web-App/main/Data/heart.csv")
# 		st.header("Fraud Prediction")
# 		return data

# 	else:
# 		#data=pd.read_csv("https://raw.githubusercontent.com/advikmaniar/ML-Healthcare-Web-App/main/Data/BreastCancer.csv")
			
# 		#data["diagnosis"] = LE.fit_transform(data["diagnosis"])
# 		data.replace([np.inf, -np.inf], np.nan, inplace=True)
# 		data["diagnosis"] = pd.to_numeric(data["diagnosis"], errors="coerce")
# 		st.header("Breast Cancer Prediction")
# 		return data

# data = get_dataset(dataset_name)



###########################################################################################################

if choice == "Try Different Models": 

	#dataset_name = st.selectbox("Select Dataset: ",('Heart Attack',"Breast Cancer"))
	classifier_name = st.selectbox("Select Classifier: ",("Logistic Regression","KNN", "Decision Trees", "Random Forest"))

	# def get_dataset(dataset_name):
	# 	if dataset_name=="Heart Attack":
	# 		bucket = "damg-project"
	# 		file_name = "card_transdata.csv"

	# 		import boto3
	# 		s3 = boto3.client('s3') 
	# 	# 's3' is a key word. create connection to S3 using default config and all buckets within S3
	# 		obj = s3.get_object(Bucket= bucket, Key= file_name) 
	# 	# get object and file (key) from bucket
	# 		data = pd.read_csv(obj['Body'])
	# 		st.write('Shape of the dataframe: ',data.shape)

	# 	#data=pd.read_csv("https://raw.githubusercontent.com/advikmaniar/ML-Healthcare-Web-App/main/Data/heart.csv")
	# 		st.header("Fraud Prediction")
	# 		return data

	# 	else:
	# 		pass

	# data = get_dataset(dataset_name)
#Getting data from s3
	import boto3
	bucket = "damg-project"
	file_name = "card_transdata.csv"
	s3 = boto3.client('s3') 
		# 's3' is a key word. create connection to S3 using default config and all buckets within S3
	obj = s3.get_object(Bucket= bucket, Key= file_name) 
		# get object and file (key) from bucket
	data = pd.read_csv(obj['Body'])
	st.write('Shape of the dataframe: ',data.shape)
	#Splitting the features and target
	x = data.drop("fraud", axis = 1).values
	y = data["fraud"].values
	#Balancing dataset
	from imblearn.over_sampling import SMOTE
	smote = SMOTE(random_state=39)
	non_fraud_over, fraud_over = smote.fit_resample(x, y)

	non_fraud_over_df = pd.DataFrame(non_fraud_over, columns=["distance_from_home", "distance_from_last_transaction",
       "ratio_to_median_purchase_price", "repeat_retailer", "used_chip",
       "used_pin_number", "online_order"])
	st.write('Data: ',non_fraud_over_df.head())
	







 
