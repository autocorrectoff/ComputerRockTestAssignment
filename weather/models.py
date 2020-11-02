from django.db import models
from datetime import datetime

# Create your models here.

class Weather(models.Model):
    description = models.CharField(max_length=160)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    visibility = models.IntegerField()
    wind = models.CharField(max_length=160)
    last_update = models.DateTimeField(default=datetime.now)