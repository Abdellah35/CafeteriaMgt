from django.forms import ModelForm
from .models import *

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ("receipt",)