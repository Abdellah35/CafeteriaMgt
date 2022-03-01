from django.contrib import admin
from .models import  Menu, Cart,Meal,Order
# Register your models here.
admin.site.register(Meal)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Cart)
