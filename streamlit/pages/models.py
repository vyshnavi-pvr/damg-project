
import streamlit as st


import requests
import ast
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
# pip install imbalanced-learn
from streamlit.web.server.websocket_headers import _get_websocket_headers

# interact with FastAPI endpoint


with st.sidebar: 
    # st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Try Different Models"])
    st.info("This project application helps you build and explore your data.")


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
	





