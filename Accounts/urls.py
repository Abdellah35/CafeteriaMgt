from django.urls import path

from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('forgotp/', views.forgotp, name="forgotp"),
    #path('chef/', views.chef, name="chef"),
    #path('casher/', views.casher, name="casher"),
    #path('waiter/', views.waiter, name="waiter"),
]
