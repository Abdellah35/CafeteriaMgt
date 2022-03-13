from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Manager(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    salary = models.IntegerField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=15)


class Employ(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, null=False)
    salary = models.IntegerField()
    phone = models.CharField(max_length=15, null=True)
    emp_type = models.CharField(max_length=20, null=False)


class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, null=False)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15, null=True)
    orders = models.IntegerField(default=0)
    total_sale = models.IntegerField(default=0)
    date_joined = models.CharField(max_length=10, null=True)


