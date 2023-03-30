from django.db import models


class Tweet(models.Model):
    term = models.CharField(max_length=70, blank=False, default='')
    data = models.JSONField
