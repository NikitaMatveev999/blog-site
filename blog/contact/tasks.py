from __future__ import absolute_import, unicode_literals
from blog.celery_app import app
from .services import send


@app.task()
def send_email(user_email):
    send(user_email)
