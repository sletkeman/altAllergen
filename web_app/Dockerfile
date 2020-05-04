FROM python:3.6.5-slim

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev unixodbc-dev

COPY api/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY api app

ENV PYTHONPATH="./app"
ENV TZ=America/New_York
EXPOSE 8080

CMD ["python", "app/main.py"]
# CMD [ "gunicorn", "-b", "0.0.0.0:8080", "--timeout", "150", "main:app" ]
