from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

#customised user model , include this model in settings
class apiUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'api_user'