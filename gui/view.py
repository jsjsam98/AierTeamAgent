from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QScrollArea,
    QSplitter,
    QTreeWidget,
    QSizePolicy,
    QLabel,
    QSpacerItem,
)
from PySide6.QtGui import QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AierTeam Kernel")

        self.resize(800, 600)

        # Layout for the chat messages
        self.messages_layout = QVBoxLayout()
        # Initial Spacer
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Widget that contains the messages layout
        self.messages_widget = QWidget()
        self.messages_widget.setLayout(self.messages_layout)

        # Scroll area for the messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.messages_widget)

        self.user_input = QLineEdit()
        self.send_button = QPushButton("Send")

        # Main layout for the chat (including messages, input, and button)
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addWidget(self.scroll_area, 1)  # Messages area
        self.chat_layout.addWidget(self.user_input)
        self.chat_layout.addWidget(self.send_button)

        # Container for the chat
        self.chat_container = QWidget()
        self.chat_container.setLayout(self.chat_layout)

        # Task list setup
        self.task_list = QTreeWidget()
        self.task_list.setHeaderLabels(["Tasks"])

        # Splitter for resizable chat and task panels
        self.splitter = QSplitter()
        self.splitter.addWidget(self.chat_container)
        self.splitter.addWidget(self.task_list)

        self.setCentralWidget(self.splitter)

    def add_message(self, message):
        item = QLabel()
        item.setText(message["content"])
        item.setWordWrap(True)
        item.adjustSize()
        item.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        item.setMinimumHeight(20)
        # Determine the background color based on the message role
        if message["role"] == "user":
            background_color = "lightblue"
        elif message["role"] == "assistant":
            background_color = "lightgreen"
        else:
            background_color = "white"  # Default color, just in case

        item.setStyleSheet(f"background-color: {background_color}")

        # Remove the spacer, add the message, then re-add the spacer at the end
        if self.spacer:
            self.messages_layout.removeItem(self.spacer)
        self.messages_layout.addWidget(item)
        self.messages_layout.addItem(self.spacer)

        # Ensure the latest message is visible
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def set_messages(self, messages):
        # Clear existing messages
        while child := self.messages_layout.takeAt(0):
            if widget := child.widget():
                widget.deleteLater()

        for message in messages:
            self.add_message(message)
