from rest_framework.decorators import api_view
from rest_framework.response import Response

from .open_ai_service import OpenAIService

from .schemas import TaskList, TaskSchema
from .models import Task
from .serializers import TaskSerializer
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def ApiOverview(request):
    # Dictionary of available API endpoints
    api_urls = {
        'API Overview': '/',
        'View All': '/all/',
        'Add': '/create/',
        'Update': '/update/pk',
        'Delete': '/pk/delete',
        'Smart Task Suggestions': '/smart_task_suggestions/',
    }

    return Response(api_urls)

@api_view(['POST'])
def add_items(request):
    item = TaskSerializer(data=request.data)

    # Check for existing data with the same fields
    if Task.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    # Validate and save the new task if data is valid
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_items(request):
    # Base query: get all tasks
    queryset = Task.objects.all()

    # Filter by id if provided
    id_param = request.query_params.get('id')

    # Filter by status or due_date if provided
    status_param = request.query_params.get('status')
    due_date_param = request.query_params.get('due_date')

    if id_param:
        queryset = queryset.filter(id=id_param)
    elif status_param:
        queryset = queryset.filter(status=status_param)
    elif due_date_param:
        queryset = queryset.filter(due_date=due_date_param)

    # Apply ordering by specified field and direction
    ordering_field = request.query_params.get('ordering_field')
    ordering_dir = request.query_params.get('ordering_dir')
    if ordering_field in ['creation_date', 'due_date']:
        if ordering_dir == 'desc':
            ordering = f'-{ordering_field}'
        else:
            ordering = ordering_field
        queryset = queryset.order_by(ordering)

    # Serialize and return data if found, otherwise return 404
    if queryset.exists():
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response({"detail": "No matching tasks found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_items(request, pk):
    # Retrieve task by primary key
    item = Task.objects.get(pk=pk)

    # Update task with new data
    data = TaskSerializer(instance=item, data=request.data)

    # Validate and save updated task
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_items(request, pk):
    # Retrieve and delete task by primary key
    item = get_object_or_404(Task, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def smart_task_suggestions(request):
    # Retrieve all tasks from the database
    items = Task.objects.all()
    list_items = []

    # Convert each task to schema format for processing
    for item in items:
        list_item = TaskSchema(
            title=item.title,
            description=item.description,
            creation_date=item.creation_date,
            due_date=item.due_date,
            status=item.status
        )
        list_items.append(list_item)

    # Generate AI-based suggestions using OpenAI service
    return Response([
        item.model_dump()
        for item in OpenAIService().generate_taks(items=list_items).items
    ])
