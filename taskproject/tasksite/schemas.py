from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

# Enum representing the allowed task statuses
class TaskStatus(str, Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'

# Pydantic model for representing a single task
class TaskSchema(BaseModel):
    title: str = Field(..., max_length=255)  # Task title, max 255 characters
    description: str  # Detailed task description
    creation_date: Optional[datetime] = None  # Optional; typically set automatically by the database
    due_date: datetime  # Required due date
    status: TaskStatus = TaskStatus.pending  # Task status, default is "pending"

    # String representation of the task (used for debugging, display, or prompting)
    def __str__(self):
        return (
            f"Task '{self.title}' with status '{self.status}' was created on "
            f"{self.creation_date.isoformat()} and is due on {self.due_date.isoformat()}. "
            f"Description: {self.description}"
        )

# Wrapper model for a list of tasks (used in responses or prompts)
class TaskList(BaseModel):
    items: List[TaskSchema]
