from flask import current_app as app
from celery.schedules import crontab
from backend.celery.tasks import email_reminder, monthly_reminder

celery_app = app.extensions['celery']

@celery_app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=13, minute=13), email_reminder.s(), name = 'Daily reminder')

    sender.add_periodic_task(crontab(hour=18, minute=58), monthly_reminder.s(), name = 'Montly reminder')
    