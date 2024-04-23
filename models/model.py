import json
import uuid
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class Message(BaseModel):
    role: str
    content: str


class Step(BaseModel):
    function: str
    args: Dict[str, Any]


class Task(BaseModel):
    task: str
    steps: List[Step]
    task_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
