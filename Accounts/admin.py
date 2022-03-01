from django.contrib import admin
from .models import Customer, Employ, Manager
# Register your models here.
admin.site.register(Customer)
admin.site.register(Employ)
admin.site.register(Manager)
