from django.db import models


class Ai_text(models.Model):
    image = models.CharField(max_length=500)
    ai_caption = models.TextField(max_length=1000, blank=True)
    ai_description = models.TextField(max_length=1000, blank=True)
