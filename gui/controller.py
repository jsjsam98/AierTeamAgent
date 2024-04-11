from gui.view import MainWindow
from gui.model import MainModel


class MainController:
    def __init__(self, model: MainModel, view: MainWindow):
        self.model = model
        self.view = view
        self.view.send_button.clicked.connect(self.add_message_from_view)

    def add_message_from_view(self):
        text = self.view.user_input.text()
        self.view.add_message({"role": "user", "content": text})
        if text:
            message = {"role": "user", "content": text}
            self.model.add_message(text)
            self.view.set_messages(self.model.messages)
            self.view.user_input.clear()
