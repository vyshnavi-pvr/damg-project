FROM python:3.9.4

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/streamlit

ADD ./streamlit /opt/streamlit
RUN pip install --upgrade pip
RUN pip install -r /opt/streamlit/requirements.txt

#add credentials
RUN mkdir -p /home/ml-api-user/.aws
COPY api/.aws/credentials /home/ml-api-user/.aws/
COPY api/.aws/config /home/ml-api-user/.aws/

RUN ls -lrt /home/ml-api-user/.aws/credentials
RUN chmod 644 /home/ml-api-user/.aws/credentials

RUN chmod +x /opt/streamlit/Main_Page.py
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

EXPOSE 8501

CMD ["streamlit", "run", "Main_Page.py"]