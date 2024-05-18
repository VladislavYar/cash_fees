import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_payments': {
        'task': 'api.v1.tasks.check_payments_celery',
        'schedule': 60.0,
    },
    'check_close_datetime_collect': {
        'task': 'api.v1.tasks.check_close_datetime_collect',
        'schedule': crontab(minute=0, hour=0),
    }
}
