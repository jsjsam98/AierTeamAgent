from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QGuiApplication
from pynput import mouse, keyboard
from app_signal.SignalManager import SignalManager

from setup import injector


class ScreenOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signal_manager = injector.get(SignalManager)
        self.setPalette(QColor(0, 0, 0, 100))  # Semi-transparent dark overlay
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(
            Qt.Window
            | Qt.X11BypassWindowManagerHint
            | Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.rectangles = []
        rect = QApplication.instance().primaryScreen().geometry()
        self.setGeometry(rect)
        self.signal_manager.add_rectangle_signal.connect(self.add_rectangle)

        # Set up global hooks
        self.listener = keyboard.Listener(on_press=self.on_key_event)
        self.listener.start()
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_event)
        self.mouse_listener.start()

    def on_key_event(self, key):
        """Handle global keyboard events."""
        self.clear_rectangles()

    def on_mouse_event(self, x, y, button, pressed):
        """Handle global mouse events."""
        if pressed:
            self.clear_rectangles()

    def add_rectangle_old(self, x, y, width, height, color=QColor(255, 255, 0, 128)):
        """Add a single rectangle to the overlay."""
        self.rectangles.append((x, y, width, height, color))
        self.update()  # Refresh the widget to show the new rectangle

    def add_rectangle(self, x, y, width, height, color=QColor(255, 255, 0, 128)):
        """Add a single rectangle to the overlay, adjusted for screen scaling."""
        screen = QGuiApplication.primaryScreen()  # Get the primary screen
        scale_factor = screen.devicePixelRatio()  # Get the scaling factor of the screen

        # Adjust coordinates and size based on the scaling factor
        scaled_x = x / scale_factor
        scaled_y = y / scale_factor
        scaled_width = width / scale_factor
        scaled_height = height / scale_factor

        # Append the scaled rectangle to the list
        self.rectangles.append((scaled_x, scaled_y, scaled_width, scaled_height, color))
        self.update()  # Refresh the widget to show the new rectangle

    def clear_rectangles(self):
        """Clear all rectangles from the overlay."""
        self.rectangles.clear()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        # Draw each rectangle
        for x, y, w, h, color in self.rectangles:
            painter.setBrush(color)
            painter.drawRect(x, y, w, h)

    def toggle_on(self):
        self.show()

    def toggle_off(self):
        self.hide()


if __name__ == "__main__":
    app = QApplication([])
    overlay = ScreenOverlay()
    overlay.show()
    overlay.add_rectangle(280, 143, 88, 13, QColor(255, 255, 0, 128))
    app.exec()
