FROM python:3.9.4

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/api

ARG PIP_EXTRA_INDEX_URL

# Install requirements, including from Gemfury
ADD ./api /opt/api
RUN pip install --upgrade pip
RUN pip install -r /opt/api/requirements.txt

#add credentials
RUN mkdir -p /home/ml-api-user/.aws
COPY api/.aws/credentials /home/ml-api-user/.aws/
COPY api/.aws/config /home/ml-api-user/.aws/

RUN ls -lrt /home/ml-api-user/.aws/credentials
RUN chmod 644 /home/ml-api-user/.aws/credentials

RUN chmod +x /opt/api/run.sh
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

EXPOSE 8001

CMD ["bash", "./run.sh"]
