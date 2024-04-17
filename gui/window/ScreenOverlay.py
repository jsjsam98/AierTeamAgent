from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor


class ScreenOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(
            parent,
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint,
        )
        self.setPalette(QColor(0, 0, 0, 100))  # Semi-transparent dark overlay
        self.setAutoFillBackground(True)
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )  # Ensure the window is translucent
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )  # Pass mouse events to underneath widgets

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 128, 128))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())  # Draw rectangle over entire widget
