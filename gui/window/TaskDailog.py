import json
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QLabel,
)


class TaskDialog(QDialog):
    def __init__(self, controller, task, parent=None):
        super().__init__(parent)
        self.set_controller(controller)
        self.task = task
        self.setWindowTitle("Edit Task")

        self.layout = QVBoxLayout(self)

        # Task name label and editor
        self.layout.addWidget(QLabel("Task Name:"))
        self.task_name_edit = QLineEdit(self.task["task"])
        self.layout.addWidget(self.task_name_edit)

        # Task steps label and editor
        self.layout.addWidget(QLabel("Task Steps (JSON):"))
        self.task_steps_edit = QTextEdit(json.dumps(self.task["steps"], indent=4))
        self.layout.addWidget(self.task_steps_edit)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_task)
        self.layout.addWidget(self.save_button)

        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(
            lambda: self.controller.handle_task_run(self.task)
        )
        self.layout.addWidget(self.run_button)

        # Smart Run button
        self.smart_run_button = QPushButton("Smart Run")
        self.smart_run_button.clicked.connect(
            lambda: self.controller.handle_task_run_smart(self.task)
        )
        self.layout.addWidget(self.smart_run_button)

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

    def set_controller(self, controller):
        from gui.controller import MainController

        self.controller: MainController = controller

    def save_task(self):
        self.task["task"] = self.task_name_edit.text()
        try:
            # Attempt to parse the edited JSON back into a list
            self.task["steps"] = json.loads(self.task_steps_edit.toPlainText())
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors (e.g., show an error message)
            print("Error parsing JSON:", e)
            # You might want to use a QMessageBox here to inform the user of the error
        self.controller.handle_task_save(self.task)
        self.accept()

    def delete_task(self):
        self.save_task()
        self.controller.handle_task_delete(self.task)
