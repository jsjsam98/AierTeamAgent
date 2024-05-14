import json
import time
from typing import List
from assistant.OpenAIAssistnat import OpenAIAssistant
from config.config import load_config
from execution.session import MainSession
from db import DataStorage
from models import Task, Message, Step
from setup import injector
from helper.NLPHelper import find_most_similar

config = load_config()


class MainModel:
    def __init__(self):
        self.session = MainSession()
        self.data_storage = injector.get(DataStorage)
        #### OPENAI ASSISTANT #####
        self.available_functions = {"run": self.session.run}
        self.assistant = OpenAIAssistant(available_functions=self.available_functions)
        ###########################
        self.messages: List[Message] = []
        self.tasks: List[Task] = []
        self.load_tasks()

    def find_similar_task(self, text):
        # find most similar function
        # convert the list of tasks to a list of strings
        tasks_str = [task.task for task in self.tasks]
        most_similar_function, similarity_score = find_most_similar(text, tasks_str)
        # retrieve the task object based on the function name
        most_similar_task = next(
            (task for task in self.tasks if task.task == most_similar_function), None
        )
        return most_similar_task, similarity_score

    def add_message(self, text):
        user_message = Message(role="user", content=text)
        self.messages.append(user_message)
        assistant_response = self.assistant.query(text)
        assistant_message = Message(
            role=assistant_response["role"], content=assistant_response["content"]
        )
        self.messages.append(assistant_message)

        # check session for task
        if len(self.session.operation_history) > 0:
            steps = []
            for step in self.session.operation_history:
                step_obj = Step(function=step["function"], args=step["args"])
                steps.append(step_obj)
            new_task = Task(task=self.session.task, steps=steps)
            self.add_task(new_task)
            # clear the task in session memory
            self.session.clear_task()
            # save task after adding
            self.save_tasks()

    def load_tasks(self):
        self.tasks = self.data_storage.get_tasks()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def delete_task(self, task_id):
        task_to_delete = self.get_task(task_id)
        if task_to_delete:
            self.tasks.remove(task_to_delete)
            self.save_tasks()
            return True
        return False

    def update_task(self, task_id, new_task: Task):
        task_to_update = self.get_task(task_id)
        if task_to_update:
            task_to_update.task = new_task.task
            task_to_update.steps = new_task.steps
            self.save_tasks()
            return True
        return False

    def save_tasks(self):
        self.data_storage.set_tasks(self.tasks)

    def run_local(self, task: Task):
        task_description = task.task   
        self.assistant.add_message("assistant", f"Running task: {task_description}")
        self.messages.append(
            Message(role="assistant", content=f"Running task: {task_description}")
        )
        self.session.run_local(task.steps)
