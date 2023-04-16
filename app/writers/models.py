from django.db import models
from posts.models import Post
from django.contrib.auth.models import User

class CollectionsHistory(models.Model):
    title = models.CharField(max_length=250)
    # coll = models.ForeignKey('posts_collections.Collection', related_name='collections', blank=False, on_delete=models.CASCADE)

class PostHistory(models.Model):
    post = models.ForeignKey('posts.Post', related_name='post_post', blank=False, on_delete=models.CASCADE)
    changed = models.DateField(auto_now=True)
    writer = models.ForeignKey(User, related_name='writer', blank=True, on_delete=models.CASCADE)
    image_field = models.TextField(max_length=500, blank=True)
    file_name = models.TextField(max_length=500,blank=True)
    collections = models.ManyToManyField(CollectionsHistory, related_name="collections_history", blank=True)