import json
import os
import uuid
from typing import List, Dict, Any

from config.config import load_config
from models import Task, Step

config = load_config()


class DataStorage:
    def __init__(self):
        self.file_path = self.create_data_path()
        self.tasks: List[Task] = self.load_tasks()

    def create_data_path(self) -> str:
        """Creates and returns the path to the data storage file."""
        appdata_path = os.getenv("APPDATA", "")
        app_folder_name = config["APP_NAME"]
        app_data_path = os.path.join(appdata_path, app_folder_name)
        os.makedirs(app_data_path, exist_ok=True)
        return os.path.join(app_data_path, config["APPDATA_TASK_FILE"])

    def save_tasks(self) -> None:
        """Saves all tasks to the JSON file specified in the configuration."""
        with open(self.file_path, "w") as file:
            json.dump([self.task_to_dict(task) for task in self.tasks], file, indent=4)
        print(f"Data saved to {self.file_path}")

    def load_tasks(self) -> List[Task]:
        """Loads all tasks from the JSON file if it exists, otherwise returns an empty list."""
        if not os.path.exists(self.file_path):
            print(f"No data file found at {self.file_path}. Returning empty list.")
            return []

        with open(self.file_path, "r") as file:
            try:
                tasks_data = json.load(file)
            except json.JSONDecodeError:
                print(
                    f"Invalid JSON data in file {self.file_path}. Returning empty list."
                )
                return []

            if not tasks_data:
                print(f"No data found in file {self.file_path}. Returning empty list.")
                return []

            tasks = [self.dict_to_task(task) for task in tasks_data]
            print(f"Data loaded from {self.file_path}")
            return tasks

    def set_tasks(self, tasks: List[Task]) -> None:
        """Sets the list of tasks to the provided list."""
        self.tasks = tasks
        # save to file after setting
        self.save_tasks()

    def get_tasks(self) -> List[Task]:
        """Returns all tasks."""
        return self.tasks

    def add_task(self, task: Task) -> None:
        """Adds a task to the list of tasks."""
        self.tasks.append(task)

    @staticmethod
    def task_to_dict(task: Task) -> Dict[str, Any]:
        """Converts a Task object to a dictionary format that can be serialized to JSON."""
        return {
            "task_id": task.task_id,
            "task": task.task,
            "steps": [
                {"function": step.function, "args": step.args} for step in task.steps
            ],
        }

    @staticmethod
    def dict_to_task(data: Dict[str, Any]) -> Task:
        """Converts a dictionary format back into a Task object.
        Generates a new UUID if 'task_id' is not provided in the input data.
        """
        # Check if 'task_id' is present in the data dictionary; if not, generate a new UUID
        task_id = data.get("task_id", str(uuid.uuid4()))

        return Task(
            task=data["task"],
            steps=[
                Step(function=step["function"], args=step["args"])
                for step in data["steps"]
            ],
            task_id=task_id,
        )
