FROM python:3.10.8-slim-buster

RUN apt-get --allow-insecure-repositories -y update && apt-get install -y sqlite3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]