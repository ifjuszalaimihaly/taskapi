from django.urls import path
from . import views

# URL patterns for task-related API views
urlpatterns = [
    # Route for API overview page
    path('', views.ApiOverview, name='home'),

    # Route to create a new task
    path('create/', views.add_items, name='add-items'),

    # Route to view all tasks (with optional filters)
    path('all/', views.view_items, name='view_items'),

    # Route to update a specific task by primary key
    path('update/<int:pk>/', views.update_items, name='update-items'),

    # Route to delete a specific task by primary key
    path('<int:pk>/delete/', views.delete_items, name='delete-items'),

    # Route to get AI-generated smart task suggestions
    path('smart_task_suggestions/', views.smart_task_suggestions, name='smart_task_suggestions'),
]
