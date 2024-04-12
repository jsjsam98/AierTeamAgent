import json
from gui.view import MainWindow
from gui.model import MainModel
from gui.window import TaskDialog


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
        self.view.add_message({"role": "user", "content": text})
        if text:
            self.model.add_message(text)
            self.view.set_messages(self.model.messages)
            self.view.user_input.clear()
        if self.model.tasks:
            self.view.set_tasks(self.model.tasks)


    def handle_task_click(self, task_name):
        print(f"Task {task_name} clicked.")
        task = next((t for t in self.model.tasks if t["task"] == task_name), None)
        if task:
            dialog = TaskDialog(self, task, self.view)
            if dialog.exec():
                self.view.set_tasks(self.model.tasks)

    def handle_task_delete(self, task):
        print(f"Deleting task: {task["task"]}")
        task = next((t for t in self.model.tasks if t["task"] == task["task"]), None)
        if task:
            print(f"Task {task["task"]} found.")
            self.model.tasks.remove(task)
            self.view.set_tasks(self.model.tasks)

    def handle_task_save(self, task):
        print(f"Saving task: {task["task"]}")
        self.model.save_tasks()

    def handle_task_run(self, task):
        print(f"Running task: {task}")
        self.model.session.run_local(task["steps"])
        print("Task completed.")

    def handle_task_run_smart(self, task):
        steps_json = json.dumps(task)
        self.model.session.run(steps_json)
        self.view.set_tasks(self.model.tasks)

    def handle_add_task(self):
        task = {"task": "New Task", "steps": []}
        dialog = TaskDialog(self, task, self.view)
        if dialog.exec():
            self.view.set_tasks(self.model.tasks)
