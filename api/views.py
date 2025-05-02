from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, TodoSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from myapp.models import Todo
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

# custom token obtain pair view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  
    
    
    
class TaskList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Todo.objects.all().order_by('id')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "responseStatus": True,
            "responseMessage": "Task created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # obj = get_object_or_404(Todo, id=self.kwargs['pk'])  # Use get_object_or_404
        #  return obj
        try:
            return Todo.objects.get(id=self.kwargs['pk'])
        except Todo.DoesNotExist:
            raise NotFound(detail="Task not found.")
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "responseStatus": True,
            "responseMessage": "Task updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "responseStatus": True,
            "responseMessage": "Task deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
        


