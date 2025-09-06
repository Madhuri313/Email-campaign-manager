import threading
import queue
import time
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Subscriber, Campaign


# Simple in-process pub-sub queue
EMAIL_QUEUE = queue.Queue()


class EmailWorker(threading.Thread):
    """Worker thread that consumes email jobs from EMAIL_QUEUE"""
    daemon = True


def __init__(self, name='worker'):
    super().__init__(name=name)
    self._stop_event = threading.Event()


def run(self):
    while not self._stop_event.is_set():
        try:
            job = EMAIL_QUEUE.get(timeout=1)
        except queue.Empty:
            continue
        try:
            send_email_job(job)
        except Exception as e:
            # In production log and optionally retry
            print('email send error', e)
        finally:
            EMAIL_QUEUE.task_done()


def stop(self):
    self._stop_event.set()


def enqueue_emails(campaign: Campaign, batch=None):
    """Enqueue email tasks for active subscribers. Optionally pass a batch of subscribers."""
    if batch is None:
        qs = Subscriber.objects.filter(is_active=True)
    else:
        qs = batch
    for sub in qs.iterator():
        EMAIL_QUEUE.put({'campaign_id': campaign.id, 'subscriber_id': sub.id})