from rest_framework import serializers
from .models import Task

# Serializer class for the Task model
# Converts between Django model instances and JSON (or other formats)
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task  # The model that this serializer is based on
        fields = '__all__'  # Include all fields from the Task model
