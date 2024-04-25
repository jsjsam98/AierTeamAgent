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
    QScrollArea,
    QLabel,
)
from PySide6.QtGui import QTextDocument
from models import Task, Message
import speech_recognition as sr


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
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: #F0F0F0;")
        self.chat_layout = QVBoxLayout(self.chat_container)

        # Setup for the scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.chat_widget = QWidget()
        # self.chat_widget.setStyleSheet("background-color: #F0F0F0;")
        self.chat_messages_layout = QVBoxLayout(self.chat_widget)
        self.scroll_area.setWidget(self.chat_widget)

        # Input elements
        self.user_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.speech_button = QPushButton("Speak")
        self.user_input.returnPressed.connect(self.send_button.click)
        self.speech_button.clicked.connect(self.handle_speech_recognition)

        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.user_input, 1)
        self.input_layout.addWidget(self.speech_button)
        self.input_layout.addWidget(self.send_button)

        # task suggestion layout
        self.task_suggestion_layout = QHBoxLayout()
        self.task_suggestion_label = QLabel()
        self.task_suggestion_label.setText("Task Suggestion:")
        self.task_suggestion_layout.addWidget(self.task_suggestion_label)

        self.chat_layout.addWidget(self.scroll_area)
        self.chat_layout.addLayout(self.task_suggestion_layout)
        self.chat_layout.addLayout(self.input_layout)

        # Add a vertical spacer to push all content to the top
        self.message_spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.chat_messages_layout.addSpacerItem(self.message_spacer)

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
        item = QLabel(f"{message.role}: {message.content}")
        item.setWordWrap(True)
        if self.message_spacer:
            self.chat_messages_layout.removeItem(self.message_spacer)
        self.chat_messages_layout.addWidget(item)
        self.chat_messages_layout.addItem(self.message_spacer)

    def set_messages(self, messages: List[Message]):
        self.clear_messages()
        for message in messages:
            self.add_message(message)

    def clear_messages(self):
        while child := self.chat_messages_layout.takeAt(0):
            if widget := child.widget():
                widget.deleteLater()

    def set_message_task(self, task: Task):
        print(f"Setting task: {task.task}")
        # clear the widget in the layout
        while child := self.task_suggestion_layout.takeAt(1):
            if widget := child.widget():
                widget.deleteLater()
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
        item.clicked.connect(lambda: self.controller.handle_task_run(task))
        self.task_suggestion_layout.addWidget(item)

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

    def handle_speech_recognition(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust the recognizer sensitivity to ambient noise and record audio
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_whisper_api(audio)
                # Add text to QLineEdit
                self.user_input.setText(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )
