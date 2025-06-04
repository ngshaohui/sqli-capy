from django.db import models

class Location(models.Model):
    location = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    rating = models.IntegerField()
    image = models.CharField(max_length=256)
    date = models.DateField()
