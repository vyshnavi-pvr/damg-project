
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
from streamlit.web.server.websocket_headers import _get_websocket_headers


plt.style.use('fivethirtyeight')
plt.style.use('dark_background')



# interact with FastAPI endpoint


import streamlit as st 
import requests
import ast



start_time=time.time()
tit1,tit2 = st.columns((4, 1))
st.set_option('deprecation.showPyplotGlobalUse', False)


# interact with FastAPI endpoint


with st.sidebar: 
    st.title("This app helps to identify any potential credit card fraud")
    st.info("This page helps data scientists explore different models with variations in parameters")




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

    RS = st.slider("Random State",0,100)
    params["RS"] = RS

    return params	

params = add_parameter_ui(classifier_name)

#Call the selected classifier
def get_classifier(clf_name,params):
    global clf
    if clf_name == "Logistic Regression":
        clf = LogisticRegression(C=params["R"],max_iter=params["MI"])

    elif clf_name == "KNN":
        clf = KNeighborsClassifier(n_neighbors=params["K"])

    elif clf_name == "Decision Trees":
        clf = DecisionTreeClassifier(max_depth=params["M"],criterion=params["C"],min_samples_split=params["SS"])

    elif clf_name == "Random Forest":
        clf = RandomForestClassifier(n_estimators=params["N"],max_depth=params["M"],criterion=params["C"])

    return clf

clf = get_classifier(classifier_name,params)

#Build the selected model
def model():

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=65)

    clf.fit(X_train,Y_train)
    Y_pred = clf.predict(X_test)
    acc=accuracy_score(Y_test,Y_pred)

    return Y_pred,Y_test

Y_pred,Y_test=model()


#Plot Outputs
def compute(Y_pred,Y_test):


    c1, c2 = st.columns((4,3))
    #Output plot
    plt.figure(figsize=(12,6))
    plt.scatter(range(len(Y_pred)),Y_pred,color="yellow",lw=5,label="Predictions")
    plt.scatter(range(len(Y_test)),Y_test,color="red",label="Actual")
    plt.title("Prediction Values vs Real Values")
    plt.legend()
    plt.grid(True)
    c1.pyplot()

    #Confusion Matrix
    cm=confusion_matrix(Y_test,Y_pred)
    class_label = ["High-risk", "Low-risk"]
    df_cm = pd.DataFrame(cm, index=class_label,columns=class_label)
    plt.figure(figsize=(12, 7.5))
    sns.heatmap(df_cm,annot=True,cmap='Pastel1',linewidths=2,fmt='d')
    plt.title("Confusion Matrix",fontsize=15)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    c2.pyplot()

    #Calculate Metrics
    acc=accuracy_score(Y_test,Y_pred)
    mse=mean_squared_error(Y_test,Y_pred)
    precision, recall, fscore, train_support = score(Y_test, Y_pred, pos_label=1, average='binary')
    st.subheader("Metrics of the model: ")
    st.text('Precision: {} \nRecall: {} \nF1-Score: {} \nAccuracy: {} %\nMean Squared Error: {}'.format(
        round(precision, 3), round(recall, 3), round(fscore,3), round((acc*100),3), round((mse),3)))


st.markdown("<hr>",unsafe_allow_html=True)
st.subheader(f"Classifier Used: {classifier_name}")
compute(Y_pred,Y_test)

#Execution Time
end_time=time.time()
st.info(f"Total execution time: {round((end_time - start_time),4)} seconds")


