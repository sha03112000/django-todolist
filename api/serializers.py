from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from myapp.models import Todo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

# Custom TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['message'] = 'Login successful'
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model() #customised user model (apiUSer model in models.py)
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        # validated_data['password'] = make_password(validated_data['password']) 
        # user = get_user_model().objects.create(**validated_data)
        # return user
        validated_data['password'] = make_password(validated_data['password'])
        # user = get_user_model().objects.create(**validated_data)
        # return user
        return super().create(validated_data)
    

class TodoSerializer(serializers.ModelSerializer):
    
    # title = serializers.CharField(
    #     validators=[UniqueValidator(queryset=Todo.objects.all(), message="Title already exists")],
    # )
    
    title = serializers.CharField()
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed','created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
    def validate_title(self, value):
        # When updating, self.instance will be set
        if Todo.objects.filter(title=value).exclude(id=getattr(self.instance, 'id', None)).exists():
            raise serializers.ValidationError("Title already exists.")
        return value
        
    
        