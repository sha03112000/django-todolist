from django.urls import path
from . import views

urlpatterns = [
    path('', views.sigIn, name='sigIn'),
    path('signUp/', views.signUp, name='signUp'),
    path('signUpAction/', views.signUpAction, name='signUpAction'),
]