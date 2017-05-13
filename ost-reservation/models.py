from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.

# class OSTUser(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.CharField(max_length=50, unique=True)
#     pw = models.CharField(max_length=100)
    
class Resource(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.TimeField('available from')
    end_time = models.TimeField('available until')
    tags = models.CharField(max_length=200, blank=True)
    last_res_made = models.DateTimeField('Last made reservation on resource')
    reserve_count = models.IntegerField(default=0)
    capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)


class Reservation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.TimeField('res start')
    end_time = models.TimeField('res end')
    date = models.DateField('res date')

