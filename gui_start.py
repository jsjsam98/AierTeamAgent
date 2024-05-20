import logging
from PySide6.QtWidgets import (
    QApplication,
)
import sys
import os
from config.config import load_config
from gui.MainController import MainController
from gui.MainModel import MainModel
from gui.MainView import MainWindow
from gui.window import ScreenOverlay
from qt_material import apply_stylesheet

logging.basicConfig(
    filename="aierteam.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


config = load_config()



def main():

    # setup openai api key
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

    app = QApplication(sys.argv)
    model = MainModel()
    window = MainWindow()
    controller = MainController(model, window)
    window.set_controller(controller)
    screen_overlay = ScreenOverlay()

    apply_stylesheet(app, theme="light_blue.xml")
    window.show()
    # screen_overlay.show()
    app.exec()

    sys.exit(0)


if __name__ == "__main__":
    main()
