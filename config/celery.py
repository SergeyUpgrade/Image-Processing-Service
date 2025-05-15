import os
from celery import Celery
from celery.signals import after_setup_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')


# Setup logging
@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.setLevel('INFO')


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
