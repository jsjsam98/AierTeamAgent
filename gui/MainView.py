from typing import List
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QHBoxLayout,
    QTextEdit,
)
from PySide6.QtGui import QTextDocument
from models import Task, Message


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AierTeam Kernel")
        self.resize(800, 600)

        # Setup for the chat messages area
        self.setupChatArea()

        # Setup for the tasks area (similar to chat but without input and send button)
        self.setupTasksArea()

        # Splitter for resizable chat and task panels
        self.main_container = QWidget()
        self.main_container_layout = QHBoxLayout(self.main_container)
        self.main_container_layout.addWidget(self.chat_container, 2)
        self.main_container_layout.addWidget(self.task_container, 1)

        self.setCentralWidget(self.main_container)

    def set_controller(self, controller):
        from gui.MainController import MainController

        self.controller: MainController = controller

    def setupChatArea(self):
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.user_input = QLineEdit()
        self.send_button = QPushButton("Send")

        self.chat_layout = QVBoxLayout()
        self.chat_layout.addWidget(self.chat_display, 1)
        self.chat_layout.addWidget(self.user_input)
        self.chat_layout.addWidget(self.send_button)

        self.chat_container = QWidget()
        self.chat_container.setLayout(self.chat_layout)

    def setupTasksArea(self):
        # Main layout that contains everything
        self.main_tasks_layout = QVBoxLayout()

        # Header layout for buttons
        self.header_layout = QHBoxLayout()
        self.add_task_button = QPushButton("Add Task")
        self.header_layout.addWidget(self.add_task_button)
        # Optionally, add more buttons to self.header_layout as needed

        # Add the header layout to the main tasks layout
        self.main_tasks_layout.addLayout(self.header_layout)

        # Task layout for individual tasks
        self.task_layout = QVBoxLayout()
        self.task_spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.task_layout.addItem(self.task_spacer)

        # Add the task layout to the main tasks layout
        self.main_tasks_layout.addLayout(self.task_layout)

        # The main container for tasks, using the main_tasks_layout
        self.task_container = QWidget()
        self.task_container.setLayout(self.main_tasks_layout)

    def add_message(self, message: Message):
        self.chat_display.append(f"{message.role}: {message.content}")

    def set_messages(self, messages: List[Message]):
        self.chat_display.clear()
        for message in messages:
            self.add_message(message)

    def add_task(self, task: Task):
        item = QPushButton()
        item.setText(task.task)
        item.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        item.setMaximumWidth(300)
        item.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #CCFFCC;
            }
        """
        )
        if self.task_spacer:
            self.task_layout.removeItem(self.task_spacer)
        self.task_layout.addWidget(item)
        self.task_layout.addItem(self.task_spacer)

        item.clicked.connect(lambda: self.controller.handle_task_click(task.task_id))

    def set_tasks(self, tasks):
        while child := self.task_layout.takeAt(0):
            if widget := child.widget():
                widget.deleteLater()

        for task in tasks:
            self.add_task(task)
