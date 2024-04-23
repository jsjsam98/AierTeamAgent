import ctypes
from ctypes import wintypes
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageGrab


class UIAutomationHelper:
    def __init__(self):
        pass

    def get_foreground_window(self):
        from pywinauto import Application

        hwnd = ctypes.windll.user32.GetForegroundWindow()
        app = Application(backend="uia").connect(handle=hwnd)
        foreground_window = app.window(handle=hwnd)
        return foreground_window

    def get_windows(self):
        from pywinauto import Desktop

        # Using the UI Automation backend
        desktop = Desktop(backend="uia")
        # Find all top-level windows
        windows = desktop.windows()
        return windows

    def get_element_tree_from_window(self, window):
        # Define the desired control types as strings
        desired_types = {
            "Button",
            "SplitButton",
            "StatusBar",
            "Tab",
            "TabItem",
            "TreeItem",
            "RadioButton",
            "MenuItem",
            "CheckBox",
            "ComboBox",
            "Custom",
            "DataItem",
            "Edit",
            "ListItem",
            "Text",
            "Image",
            "ScrollBar",
            "Slider",
        }

        elements = []
        for elem in window.descendants():
            # Use .element_info.control_type to get the control type of the element
            if (
                elem.element_info.control_type in desired_types
                and elem.element_info.visible
            ):
                try:
                    if elem.window_text():
                        elements.append(elem)
                except Exception as ex:
                    print(f"Exception when processing element: {ex}")
        return elements

    def screenshot_window_with_masks(self, window, elements):
        # Take a screenshot of the entire window
        screen = ImageGrab.grab()
        # Draw masks over detected elements
        draw = ImageDraw.Draw(screen)
        for ele in elements:
            rect = ele.element_info.rectangle
            draw.rectangle(
                [rect.left, rect.top, rect.right, rect.bottom],
                outline="red",
                width=3,
            )

        # Ensure the images folder exists
        images_folder = os.path.join(os.getcwd(), "images")
        os.makedirs(images_folder, exist_ok=True)

        # Save the image with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screen.save(os.path.join(images_folder, f"{timestamp}.png"))
