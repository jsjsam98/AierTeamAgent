from PySide6.QtWidgets import (
    QApplication,
)
from PySide6.QtGui import QColor  # Import QColor for setting item colors
import sys

from gui.controller import MainController
from gui.model import MainModel
from gui.view import MainWindow


def main():

    app = QApplication(sys.argv)
    model = MainModel()
    window = MainWindow()
    controller = MainController(model, window)

    window.set_controller(controller)
    window.show()
    app.exec()

    sys.exit(0)


if __name__ == "__main__":
    main()
