import logging
from abc import ABC, abstractmethod
import json
import pyautogui
import re
from typing import List
from DevAPIClient import DevAPIClient
from UIAutomationHelper import UIAutomationHelper
import time

# pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1


class Rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class ElementDetail:
    def __init__(self, automation_id: str, name: str, type: str, rect: Rect):
        self.automation_id = automation_id
        self.name = name
        self.type = type
        self.rect = rect


class ElementBrief:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type


class Action(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class Click(Action):
    def __init__(self, x, y, button, agent):
        self.x = int(x)
        self.y = int(y)
        self.button = button
        self.agent = agent

    def execute(self):
        self.agent.click(self.x, self.y, self.button)


class MoveTo(Action):
    def __init__(self, x, y, agent):
        self.x = int(x)
        self.y = int(y)
        self.agent = agent

    def execute(self):
        self.agent.move_to(self.x, self.y)


class Type(Action):
    def __init__(self, text, agent):
        self.text = text
        self.agent = agent

    def execute(self):
        self.agent.type(self.text)


class Scroll(Action):
    def __init__(self, direction, times, agent):
        self.amount = int(times) * (120 if direction == "up" else -120)
        self.agent = agent

    def execute(self):
        self.agent.scroll(self.amount)


class Press(Action):
    def __init__(self, keys, agent):
        self.keys = keys
        self.agent = agent

    def execute(self):
        self.agent.press(self.keys)


class ClickItem(Action):
    def __init__(self, item, agent):
        self.item = item
        self.agent = agent

    def execute(self):
        self.agent.click_item(self.item)


class ExecutionAgent:

    def __init__(self):

        self.element_details: List[ElementDetail] = []
        self.command_history = []
        self.command_dictionary = {
            r"^click (left|right|middle) (\d+),(\d+)$": Click,
            r"^move mouse to (\d+),(\d+)$": MoveTo,
            r"^type (.*)$": Type,
            r"^press (.*)$": Press,
            r"^scroll (up|down) (\d+) times$": Scroll,
            r"^click item: (.*)$": ClickItem,
        }
        self.api_client = DevAPIClient()

    def execute_command(self, command):
        try:
            for pattern, command_class in self.command_dictionary.items():
                match = re.match(pattern, command)
                if match:
                    action: ExecutionAgent.Action = command_class(*match.groups(), self)
                    action.execute()
                    self.command_history.append(command)
                    print(f"Command '{command}' executed")
        except Exception as e:
            print(e)
            print(f"Command '{command}' failed")

    def click(self, x, y, button="left"):
        pyautogui.click(x, y, button)

    def move_to(self, x, y):
        pyautogui.moveTo(x, y)

    def drag_to(self, x, y, duration=1):
        pyautogui.dragTo(x, y, duration=duration)

    def type(self, text):
        pyautogui.typewrite(text)

    def press(self, keys):
        pyautogui.press(keys)

    def scroll(self, direction, times):
        pyautogui.scroll(times * (120 if direction == "up" else -120))

    def click_item(self, item_name):
        element = next((e for e in self.element_details if e.name == item_name), None)
        if element:

            # Click on the element
            pyautogui.click(
                element.rect.left + (element.rect.right - element.rect.left) / 2,
                element.rect.top + (element.rect.bottom - element.rect.top) / 2,
            )
        else:
            print(f"Element '{item_name}' not found")

    def search(self, query, screenshot=""):
        result = self.api_client.get_command_gpt_4(query, screenshot)
        return result

    def search_and_execute(self, query):
        i = 0
        result = ""
        while i < 10 and result != "none":
            window = UIAutomationHelper.get_foreground_window()
            uia_elements = UIAutomationHelper.get_element_tree_from_window(window)
            self.element_details = [
                ElementDetail(
                    ele.element_info.automation_id,
                    ele.element_info.name,
                    ele.element_info.control_type,
                    Rect(
                        ele.element_info.rectangle.left,
                        ele.element_info.rectangle.top,
                        ele.element_info.rectangle.right,
                        ele.element_info.rectangle.bottom,
                    ),
                )
                for ele in uia_elements
            ]
            element_briefs = [
                {
                    "name": ele.element_info.name,
                    "control_type": ele.element_info.control_type,
                }
                for ele in uia_elements
            ]
            element_briefs_json = json.dumps(element_briefs)
            # limit the json to 2000 characters
            element_briefs_json = element_briefs_json[:2000]
            result = self.search(query, element_briefs_json)
            self.execute_command(result)
            i += 1
            # wait for 2 seconds
            time.sleep(2)
        self.api_client.print_cost()
        print("Done")
        logging.info(f"Message History: {self.api_client.messages}")
