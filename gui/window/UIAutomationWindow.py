import sys
import os
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from pynput import mouse, keyboard
from pywinauto import Desktop
from PIL import ImageGrab
from PySide6.QtCore import Qt


class UIAutomationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("UI Automation Helper")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(layout)

        self.infoLabel = QLabel("Select an element using Ctrl+Left Click", self)
        self.infoLabel.setWordWrap(True)
        layout.addWidget(self.infoLabel)

        self.screenshotLabel = QLabel(self)
        self.screenshotLabel.setFixedSize(300, 200)
        layout.addWidget(self.screenshotLabel)

    def handle_element_selection(self, x, y):
        desktop = Desktop(backend="uia")
        try:
            element = desktop.from_point(x, y)
            if element:
                process_id = element.process_id()
                proc = psutil.Process(process_id)
                exe_name = os.path.basename(proc.exe())

                info_text = (
                    f"Process Name: {exe_name}\n"
                    f"Control Type: {element.element_info.control_type}\n"
                    f"Name: {element.element_info.name}"
                )
                self.infoLabel.setText(info_text)

                bbox = (
                    element.rectangle().left,
                    element.rectangle().top,
                    element.rectangle().right,
                    element.rectangle().bottom,
                )
                screenshot = ImageGrab.grab(bbox)
                screenshot.save("element_screenshot.png")
                pixmap = QPixmap("element_screenshot.png")
                self.screenshotLabel.setPixmap(
                    pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
        except Exception as e:
            self.infoLabel.setText(f"Failed to select element: {e}")


# Global state to track whether the control key is currently pressed
ctrl_pressed = False


def on_click(x, y, button, pressed):
    global ctrl_pressed
    if pressed and button == mouse.Button.left and ctrl_pressed:
        window.handle_element_selection(x, y)


def on_press(key):
    global ctrl_pressed
    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = True
    except AttributeError:
        pass


def on_release(key):
    global ctrl_pressed
    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = False
    except AttributeError:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UIAutomationWindow()
    window.show()

    # Set up listeners for mouse and keyboard
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()

    sys.exit(app.exec())
