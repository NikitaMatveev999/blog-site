FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN python manage.py collectstatic --noinput

CMD gunicorn blog.wsgi:application -b 0.0.0.0:8000
#CMD celery -A blog worker -l info --concurrency 4
