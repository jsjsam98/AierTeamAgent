import json
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont

from models import Task, Step


class TaskDialog(QDialog):
    def __init__(self, controller, task: Task, parent=None):
        super().__init__(parent)
        self.task: Task = task
        self.setFixedSize(QSize(400, 600))
        self.set_controller(controller)
        self.setWindowTitle("Edit Task")

        self.main_layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        # Task name label and editor
        self.left_layout.addWidget(QLabel("Task Name:"))
        self.task_name_edit = QLineEdit(self.task.task)
        self.left_layout.addWidget(self.task_name_edit)

        # Task steps label and editor
        self.left_layout.addWidget(QLabel("Task Steps (JSON):"))
        steps_list = [step.model_dump() for step in self.task.steps]
        formatted_json = "<pre>" + json.dumps(steps_list, indent=4) + "</pre>"
        self.task_steps_edit = QTextEdit(formatted_json)
        self.left_layout.addWidget(self.task_steps_edit)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_task)
        self.left_layout.addWidget(self.save_button)

        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(
            lambda: self.controller.handle_task_run(self.task)
        )
        self.left_layout.addWidget(self.run_button)

        # Smart Run button
        self.smart_run_button = QPushButton("Smart Run")
        self.smart_run_button.clicked.connect(
            lambda: self.controller.handle_task_run_smart(self.task)
        )
        self.left_layout.addWidget(self.smart_run_button)

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_task)
        self.left_layout.addWidget(self.delete_button)

    def set_controller(self, controller):
        from gui.MainController import MainController

        self.controller: MainController = controller

    def on_item_clicked(self, item):
        action = item.text()
        if action == "click_item":
            self.click_item_clicked(item)
        elif action == "type":
            self.type_clicked(item)
        elif action == "press":
            self.press_clicked(item)

    def click_item_clicked(self, item):
        print("click_item action triggered with task:", item.text())

    def type_clicked(self, item):
        print("type action triggered with task:", item.text())

    def press_clicked(self, item):
        print("press action triggered with task:", item.text())

    def save_task(self):
        self.task.task = self.task_name_edit.text()
        try:
            # Attempt to parse the edited JSON back into a list
            json_text = self.task_steps_edit.toPlainText()
            parsed_steps = json.loads(json_text)

            # Create a list comprehension to parse each dictionary into a Step object
            steps_list = [Step.model_validate(step_data) for step_data in parsed_steps]

            # Assign the list of Step objects to self.task.steps
            self.task.steps = steps_list
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors (e.g., show an error message)
            print("Error parsing JSON:", e)
            # You might want to use a QMessageBox here to inform the user of the error
        self.controller.handle_task_save(self.task)
        self.accept()

    def delete_task(self):
        self.controller.handle_task_delete(self.task.task_id)
        self.accept()
