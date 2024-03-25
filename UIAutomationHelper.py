import ctypes
from ctypes import wintypes
from pywinauto import Desktop, Application
from pywinauto.uia_defines import IUIA


class UIAutomationHelper:
    def __init__(self):
        # all static method
        pass

    @staticmethod
    def get_foreground_window():
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        app = Application(backend="uia").connect(handle=hwnd)
        foreground_window = app.window(handle=hwnd)
        return foreground_window

    @staticmethod
    def get_windows():
        # Using the UI Automation backend
        desktop = Desktop(backend="uia")
        # Find all top-level windows
        windows = desktop.windows()
        return windows

    @staticmethod
    def get_element_tree_from_window(window):
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
