from PySide6.QtCore import QObject, Signal


class SignalManager(QObject):
    # Define all the signals you expect to use in the application
    add_rectangle_signal = Signal(int, int, int, int)

    def __init__(self):
        super().__init__()

    def add_rectangle(self, x, y, width, height):
        self.add_rectangle_signal.emit(x, y, width, height)
