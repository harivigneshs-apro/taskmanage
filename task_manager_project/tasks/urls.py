from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle-status/', views.task_toggle_status, name='task_toggle_status'),
    
    # Tag URLs
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
]
