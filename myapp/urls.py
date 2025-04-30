from django.urls import path
from . import views

urlpatterns = [
    path('', views.sigIn, name='sigIn'),
    path('signInAction/', views.signInAction, name='signInAction'),
    path('signUp/', views.signUp, name='signUp'),
    path('signUpAction/', views.signUpAction, name='signUpAction'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout_view'),
    path('addNew/', views.addTodo, name='addTodo'),
    path('addNewAction/', views.addTodoAction, name='addNewAction'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('updateAction/', views.updateAction, name='updateAction'),
]