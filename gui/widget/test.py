from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QLabel

from ClickableLabel import ClickableLabel

# Example usage
if __name__ == "__main__":
    app = QApplication([])

    # Main window setup
    main_window = QWidget()
    main_window.resize(800, 600)
    main_layout = QVBoxLayout(main_window)

    # Scroll area setup
    scroll_area = QScrollArea(main_window)
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    # Clickable label setup
    clickable_label = ClickableLabel(
        "This is a very long text that should wrap inside the label, making the entire area clickable. "
        * 20
    )
    clickable_label.clicked.connect(lambda: print("Label Clicked!"))

    # Adding the clickable label to the scroll area
    scroll_area.setWidget(clickable_label)

    # Adding the scroll area to the main layout
    main_layout.addWidget(scroll_area)

    main_window.show()
    app.exec()
