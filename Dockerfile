FROM python:3.13-slim

WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4" ]