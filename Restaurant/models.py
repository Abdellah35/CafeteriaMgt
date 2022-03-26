from django.db import models
from Accounts.models import *
# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    img = models.ImageField(upload_to='pics')


class Meal(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    desc = models.TextField(max_length=50)
    img = models.ImageField(upload_to='pics')
    menu =models.ForeignKey(Menu, on_delete=models.CASCADE)


    
class Order(models.Model):
    customer =models.ForeignKey(User, on_delete=models.CASCADE)
    chef = models.CharField(max_length=50)
    waiter = models.CharField(max_length=50)
    item = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date = models.CharField(max_length=10)
    address = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=20, null=True)
    price = models.CharField(max_length=20, null=True)
    receipt = models.ImageField(upload_to='receipts')
    delivery = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    is_picked = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    is_blocked= models.BooleanField(default=False)


class Cart(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    customer = models.CharField(max_length=50)
    img = models.ImageField(upload_to='pics')
    quantity = models.IntegerField()
