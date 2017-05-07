from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    pw = models.CharField(max_length=100)
    
class Resource(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField('available from')
    end_time = models.DateTimeField('available until')
    tags = models.CharField(max_length=200)
    url = models.CharField(max_length=100)

    
class Reservations(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField('res start')
    end_time = models.DateTimeField('res end')


