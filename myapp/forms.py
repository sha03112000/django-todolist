from django.contrib.auth.hashers import make_password
from django import forms
from .models import Login
import re

# Form for creating a product
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Login.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Login.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError("Invalid email format!")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^[a-zA-Z0-9_.+-]{8,}$', password):
            raise forms.ValidationError("Password must be at least 8 characters long!")
        return make_password(password)
        

# Form for updating a product
# class UpdateProductForm(forms.ModelForm):
#     class Meta:
#         model = Login
#         fields = ['name', 'price']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['price'].required = False  # Price is optional for updates
