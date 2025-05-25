from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

class TaskStatus(str, Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'

class TaskSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    creation_date: Optional[datetime] = None  # optional for creation (auto-generated in DB)
    due_date: datetime
    status: TaskStatus = TaskStatus.pending


    def __str__(self):
        return (
            f"Task '{self.title}' with status '{self.status}' was created on "
            f"{self.creation_date.isoformat()} and is due on {self.due_date.isoformat()}. "
            f"Description: {self.description}"
        )

class TaskList(BaseModel):
    items: List[TaskSchema]