from django.db import models


class Non_approved(models.Model):
    name = models.CharField(unique=True, max_length=250, null=None)

    def __str__(self) -> str:
        return f"{self.name}"
