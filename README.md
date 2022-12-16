# DAMG Project:  Credit Card Fraud Detection

### DAMG 7245 - Big Data and Intelligent Analytics 
### Fall Semester 2022
---------------------------------------------------------------------------------------------------------------------------------------------


#### Team 2  Information:

| NAME                  |     NUID        |
|-----------------------|-----------------|
| Vyshnavi Pendru       |   002919813     |
| Moksha Ajaykumar Doshi|   002922797     |


**Project Proposal link - 
Google Codelabs - [https://codelabs-preview.appspot.com/?file_id=1qNgCSdMase7BZ0hIgzXX3MoG30t2BKT-CcIxz5PYo1c#8](https://codelabs-preview.appspot.com/?file_id=1qNgCSdMase7BZ0hIgzXX3MoG30t2BKT-CcIxz5PYo1c#0)

https://drive.google.com/drive/folders/1R32qu0MoUBC8avR23ProxYCg6grsVlOo

Storing data in AWS S3 bucket and retrieving it, Docker , FastAPI - Vyshnavi Pendru

Validation of data using Great Expectations, Data Science, EDA, Modeling & Analysis, Model-as-a-service in FastAPI, Analysis & Model in Streamlit - Moksha Doshi
+damg-project
|   docker-compose.yml
|   eda.ipynb
|   LICENSE
|   output.doc
|   README.md
|   tasklist.md
|   Untitled.ipynb
|   
+---api
|   |   Dockerfile
|   |   model-as-a-service.py
|   |   model.pkl
|   |   requirements.txt
|   |   run.sh
|   |   
|   +---.aws
|   |       config
|   |       credentials
|   |       
|   \---__pycache__
|           model-as-a-service.cpython-37.pyc
|           
+---data
|   |   card_transdata.csv
|   |   eda.ipynb
|   |   Untitled.ipynb
|   |   
|   \---.ipynb_checkpoints
|           eda-checkpoint.ipynb
|           Untitled-checkpoint.ipynb
|           
+---datascience
|   |   create_model.py
|   |   credit_card_eda_models.ipynb
|   |   datascience.ipynb
|   |   model.pkl
|   |   pickle_model.pkl
|   |   
|   \---.ipynb_checkpoints
|           datascience-checkpoint.ipynb
|           Untitled-checkpoint.ipynb
|           
+---Great_expectaion_on_data
|       ge_card_trans.html
|       
+---streamlit
|   |   Dockerfile
|   |   login.py
|   |   Main_Page.py
|   |   requirements.txt
|   |   
|   +---.aws
|   |       config
|   |       credentials
|   |       
|   \---pages
|           Data_Statistics.py
|           Manually_Checking_Predictions.py
|           Try_Different_Models.py
|           
\---util
        get_data_s3.py
        
