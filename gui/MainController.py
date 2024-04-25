import json
from gui.MainView import MainWindow
from gui.MainModel import MainModel
from gui.window import TaskDialog
from models import Task, Message


class MainController:
    def __init__(self, model: MainModel, view: MainWindow):
        self.model = model
        self.view = view
        self.view.send_button.clicked.connect(self.handle_add_message)
        self.view.add_task_button.clicked.connect(self.handle_add_task)

        ## Init views
        self.view.set_tasks(self.model.tasks)

    def handle_add_message(self):
        text = self.view.user_input.text()
        if text:
            # handle message
            self.model.add_message(text)
            self.view.set_messages(self.model.messages)
            self.view.user_input.clear()

            # handle task
            most_similar_task, similarity_score = self.model.find_similar_task(text)
            if similarity_score > 0.1:
                self.view.set_message_task(most_similar_task)

        if self.model.tasks:
            self.view.set_tasks(self.model.tasks)

    def handle_add_task(self):
        task = Task(task="New Task", steps=[])
        self.model.tasks.append(task)
        dialog = TaskDialog(self, task, self.view)
        if dialog.exec():
            self.view.set_tasks(self.model.tasks)
            self.model.save_tasks()

    def handle_task_click(self, task_id):
        task = self.model.get_task(task_id)
        print(f"Task {task.task} clicked.")
        if task:
            dialog = TaskDialog(self, task, self.view)
            if dialog.exec():
                self.view.set_tasks(self.model.tasks)

    def handle_task_delete(self, task_id):
        task = next((t for t in self.model.tasks if t.task_id == task_id), None)
        print(f"Deleting task: {task.task}")
        if task:
            print(f"Task {task.task} found.")
            self.model.delete_task(task_id)
            self.view.set_tasks(self.model.tasks)

    def handle_task_save(self, task: Task):
        print(f"Saving task: {task.task}")
        self.model.save_tasks()

    def handle_task_run(self, task: Task):
        print(f"Running task: {task}")
        self.model.session.run_local(task.steps)
        print("Task completed.")

    def handle_task_run_smart(self, task: Task):
        steps_dicts = [step.model_dump() for step in task.steps]
        steps_json = json.dumps(steps_dicts)

        self.model.session.run(steps_json)
        self.view.set_tasks(self.model.tasks)
