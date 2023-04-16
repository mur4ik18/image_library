from django.db import models


class IgnoreList(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ['title']
