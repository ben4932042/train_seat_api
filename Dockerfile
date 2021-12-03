FROM python:3.6-slim

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt 
RUN apt-get update -y &&  apt-get install curl -y

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
