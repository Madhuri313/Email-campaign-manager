from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True) # becomes False when unsubscribed
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.email} ({'Active' if self.is_active else 'Inactive'})"


class Campaign(models.Model):
    subject = models.CharField(max_length=255)
    preview_text = models.CharField(max_length=512, blank=True)
    article_url = models.URLField(blank=True)
    html_content = models.TextField(blank=True)
    plain_text_content = models.TextField(blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)


def __str__(self):
    return f"{self.subject} ({self.published_date.date()})"