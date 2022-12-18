FROM python:3.9
WORKDIR /locust
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8089