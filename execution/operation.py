from typing import Iterable
import pyautogui


def click(self, x: int, y: int, button: str = "left"):
    pyautogui.click(x, y, button)


def move_to(self, x, y):
    pyautogui.moveTo(x, y)


def drag_to(self, x, y, duration=1):
    pyautogui.dragTo(x, y, duration=duration)


def type(self, text):
    pyautogui.typewrite(text)


def press(self, keys: str | Iterable[str]):
    pyautogui.press(keys)


def scroll(self, direction, times):
    pyautogui.scroll(times * (120 if direction == "up" else -120))

def click_item(self, item):
    pass