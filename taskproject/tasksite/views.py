from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)

@api_view(['POST'])
def add_items(request):
    item = TaskSerializer(data=request.data)

    # validating for already existing data
    if Task.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_items(request):
    # Base query: get all tasks
    queryset = Task.objects.all()

    # Filtering by id
    id_param = request.query_params.get('id')

    # Filtering by status and due_date (exact match)
    status_param = request.query_params.get('status')
    due_date_param = request.query_params.get('due_date')

    if id_param:
        queryset = queryset.filter(id=id_param)
    elif status_param:
        queryset = queryset.filter(status=status_param)
    elif due_date_param:
        queryset = queryset.filter(due_date=due_date_param)

    # Ordering by creation_date or due_date (ascending or descending)
    ordering_field = request.query_params.get('ordering_field')
    ordering_dir = request.query_params.get('ordering_dir')
    if ordering_field in ['creation_date', 'due_date']:
        if ordering_dir == 'desc':
            ordering = f'-{ordering_field}'
        else:
            ordering = ordering_field
        queryset = queryset.order_by(ordering)

    # Return results if any, otherwise return 404
    if queryset.exists():
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response({"detail": "No matching tasks found."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def update_items(request, pk):
    item = Task.objects.get(pk=pk)
    data = TaskSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Task, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)