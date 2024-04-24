import ctypes
from ctypes import wintypes
from datetime import datetime
from io import StringIO
import logging
import os
from PIL import Image, ImageDraw, ImageGrab
from collections import deque


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

    def get_elements_bfs(self, root_element):
        all_elements = []
        queue = deque([root_element])  # Initialize queue with the root element

        while queue:
            current_element = queue.popleft()  # Remove and return the leftmost element
            children = current_element.children()  # Get children of the current element

            if children:
                queue.extend(children)  # Add children to the right side of the queue
                all_elements.extend(children)  # Add children to the results list

        return all_elements

    def get_element_tree_from_window_recursive(self, window):
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
        uia_elements = self.get_elements_bfs(window)
        for elem in uia_elements:
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
            "Pane",
        }

        window.print_control_identifiers(depth=25)

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

    def select_element_from_point(self, x, y):
        from pywinauto import Desktop

        desktop = Desktop(backend="uia")
        try:
            element = desktop.from_point(x, y)
            return element
        except Exception as ex:
            print(f"No element found at point ({x}, {y}): {ex}")
            return None
