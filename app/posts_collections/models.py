from django.db import models
from posts.models import Post
from django.contrib.auth.models import User

# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=250)
    for_changing = models.BooleanField(default=0)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    def __str__(self) -> str:
        return f"{self.title}"