from aeon.celery import app
from django_email_verification import send_email

@app.task
def send_confirming_email(user):
    send_email(user)
    return {'status': True}