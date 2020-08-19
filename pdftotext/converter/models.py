from django.db import models

# Create your models here.
class history(models.Model):
    url = models.CharField(max_length=200)
    data = models.CharField(max_length=2500)