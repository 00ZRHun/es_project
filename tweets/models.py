from django.db import models


class Tweet(models.Model):
    data = models.JSONField
