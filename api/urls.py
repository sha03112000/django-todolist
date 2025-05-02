from django.urls import path
from . import views



urlpatterns = [
    path('lists/', views.TaskList.as_view(), name='create_view_task'),
    path('lists/<int:pk>', views.TaskDetail.as_view(), name='detail_view_delete_update'),
]