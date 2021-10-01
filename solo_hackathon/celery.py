import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solo_hackathon.settings')

app = Celery('solo_hackathon')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
