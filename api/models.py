from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    imdb_id = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    poster = models.CharField(max_length=500)

    def __str__(self):
        return self.title
