FROM python:3.11
ADD . /app
WORKDIR /app
RUN pip install -r to-do-app/requirements.txt