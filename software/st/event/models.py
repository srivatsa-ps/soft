from django.db import models

# Create your models here.
class eventhall(models.Model):
     firstname = models.CharField(max_length=255)
     apartment = models.CharField(max_length=255)
     purp = models.CharField(max_length=255)
     edate = models.DateField()
     stime=models.TimeField()
     


