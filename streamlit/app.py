import streamlit as st 
import requests
import ast
import pandas as pd
import pandas_profiling
import seaborn as sns
import time
import matplotlib.pyplot as plt
from streamlit_pandas_profiling import st_profile_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support as score, mean_squared_error
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.decomposition import PCA



# interact with FastAPI endpoint


import streamlit as st 
import requests
import ast

start_time=time.time()
tit1,tit2 = st.columns((4, 1))
st.set_option('deprecation.showPyplotGlobalUse', False)


with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("UI interface for Model as a service")
    choice = st.radio("Navigation", ["Home Page","Profiling Any Dataset","Manually Checking Predictions", "Statics", "Try Different Models"])
    
    st.info("This project application helps you build and explore your data.")

if choice == "Home Page":
    st.title("Basic training of a simple ML Regression model using a single feature/predictor/input")
    
	headers = {'accept': 'application/json',}
		data = {'grant_type': '','username': '{user_val}'.format(user_val=username),'password': '{pass_val}'.format(pass_val=password),'scope': '','client_id': '' ,'client_secret': '',}
		response = requests.post('http://127.0.0.1:8000/token', headers=headers, data=data)
		string_response = response.content.decode("utf-8") 
		dict_response = ast.literal_eval(string_response)
		auth_token = dict_response['access_token']	

		json_response = response.json()
		
		st.session_state['access_token'] = json_response["access_token"]
		st.session_state['token_type'] = json_response["token_type"]

		headers = {'accept': 'application/json','Authorization': 'Bearer {access_token}'.format(access_token=auth_token),}	
			
		st.success("Loggedin")
		
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



if choice == "Try Different Models": 

	classifier_name = st.selectbox("Select Classifier: ",("Logistic Regression","KNN", "Decision Trees", "Random Forest"))

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
	#st.write('Data: ',non_fraud_over_df.head())

	non_fraud_over_df["fraud"] = fraud_over
	df3 = non_fraud_over_df
	st.write('Data: ',df3.head())

	feature_columns = ["distance_from_home", "distance_from_last_transaction",
		"ratio_to_median_purchase_price", "repeat_retailer", "used_chip", "used_pin_number", "online_order"]
	X = df3[feature_columns]
	y = df3.fraud


	#select classifier 
	def add_parameter_ui(clf_name):
		params={}
		st.write("Select values: ")

		if clf_name == "Logistic Regression":
			R = st.slider("Regularization",0.1,10.0,step=0.1)
			MI = st.slider("max_iter",50,400,step=50)
			params["R"] = R
			params["MI"] = MI

		elif clf_name == "KNN":
			K = st.slider("n_neighbors",1,20)
			params["K"] = K

		elif clf_name == "Decision Trees":
			M = st.slider("max_depth", 2, 20)
			C = st.selectbox("Criterion", ("gini", "entropy"))
			SS = st.slider("min_samples_split",1,10)
			params["M"] = M
			params["C"] = C
			params["SS"] = SS

		elif clf_name == "Random Forest":
			N = st.slider("n_estimators",50,500,step=50,value=100)
			M = st.slider("max_depth",2,20)
			C = st.selectbox("Criterion",("gini","entropy"))
			params["N"] = N
			params["M"] = M
			params["C"] = C

		RS = st.sidebar.slider("Random State",0,100)
		params["RS"] = RS

		return params	

	params = add_parameter_ui(classifier_name)

	








 
