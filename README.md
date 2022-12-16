# DAMG Project:  Credit Card Fraud Detection


### DAMG 7245 - Big Data and Intelligent Analytics 
### Fall Semester 2022
---------------------------------------------------------------------------------------------------------------------------------------------


#### Team 2  Information:

| NAME                  |     NUID        |
|-----------------------|-----------------|
| Vyshnavi Pendru       |   002919813     |
| Moksha Ajaykumar Doshi|   002922797     |


**Project Proposal link** - 
Google Codelabs - [https://codelabs-preview.appspot.com/?file_id=1qNgCSdMase7BZ0hIgzXX3MoG30t2BKT-CcIxz5PYo1c#8](https://codelabs-preview.appspot.com/?file_id=1qNgCSdMase7BZ0hIgzXX3MoG30t2BKT-CcIxz5PYo1c#0)

**Project Documentation link**- 
Google Codelabs - https://codelabs-preview.appspot.com/?file_id=1OLQHLza5rEUGrf1w3VChJf5XYeAgSyagsfMOCwpWkmI#0

**Project Demo link**- https://drive.google.com/drive/folders/1R32qu0MoUBC8avR23ProxYCg6grsVlOo

**Project link which is deployed on aws ec2 instance**-https://test.nedamg7245fall2022.com/

To Predict whether a given transaction is fraud or not, we have created an streamlit application with backend using fastapi and authenticating with OAuth2 Authentication. Then dockerized both frontend and backend by deploying on AWS EC2 instance .

**Steps to Run the Application**

- Install Docker and Docker Compose
- git clone https://github.com/vyshnavi-pvr/damg-project
- cd damg-project
- add credentials in api/.aws and streamlit/.aws
- sudo docker-compose up -d --build
- The streamlit application runs on 8501 port and fastpi run on 8001 port



Storing data,model in AWS S3 bucket and retrieving it, Docker , Authentication and Prediction in FastAPI, Authentication in Streamlit, Deploying on AWS - Vyshnavi Pendru

Validation of data using Great Expectations, Data Science, EDA, Modeling & Analysis, Model-as-a-service in FastAPI, Analysis & Model in Streamlit - Moksha Doshi

>   docker-compose.yml
>   
+---api
>   >   
>   >   Dockerfile
>   >   
>   >   model-as-a-service.py
>   >   
>   >   model.pkl
>   >   
>   >   requirements.txt
>   >   
>   >   run.sh
>   >   
>   +---.aws
>   >   
>   >    config
>   >   
>   >    credentials
>   >       
+---datascience
>   >   
>   >   create_model.py
>   >   
>   >   credit_card_eda_models.ipynb
>   >   
>   >   datascience.ipynb
>   >   
>   >   model.pkl
>   >   
>   >   pickle_model.pkl
>   >   
+---Great_expectaion_on_data
>   >   
>   >   ge_card_trans.html
>   >       
+---streamlit
>   >   
>   >   Dockerfile
>   >   
>   >   login.py
>   >   
>   >   Main_Page.py
>   >   
>   >   requirements.txt
>   >   
>   +---.aws
>   >    config
>   >   
>   >    credentials
>   >       
>   +---pages
>   >   >   Data_Statistics.py
>   >   >       
>   >   >  Manually_Checking_Predictions.py
>   >   >  
>   >   >   Try_Different_Models.py
>   >   >        
+---util
>   >    get_data_s3.py
        
