from django.db import models

# Define the Task model representing a single to-do item.
class Task(models.Model):

    # Enum for allowed task statuses
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    # Title of the task (max 255 characters)
    title = models.CharField(max_length=255)

    # Detailed description of the task
    description = models.TextField()

    # Timestamp when the task was created (automatically set once)
    creation_date = models.DateTimeField(auto_now_add=True)

    # Deadline for the task to be completed
    due_date = models.DateTimeField()

    # Current status of the task, must be one of the predefined choices
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # String representation of the model (used in admin, shell, etc.)
    def __str__(self):
        return self.title
