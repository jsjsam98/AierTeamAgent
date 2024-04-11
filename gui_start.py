from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QListWidget,
    QListWidgetItem,  # Import QListWidgetItem for custom list items
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
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
