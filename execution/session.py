import json
import logging
from time import sleep
from typing import Iterable, List

from config.config import load_config
from openai import OpenAI

from execution.model import ItemDetail, Rect
from helper import OCRHelper, UIAutomationHelper


config = load_config()


class MainSession:
    def __init__(self):
        self.client = OpenAI(api_key=config["OPENAI_API_KEY"])
        self.ocr_helper = OCRHelper()
        self.uiautomation_helper = UIAutomationHelper()
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.cost = 0
        self.model = config["AUTO_MODEL"]
        self.is_running = False
        self.max_step = 20
        self.item_details: List[ItemDetail] = []
        self.tools = []
        self.operation_history = []
        self.available_functions = {
            "click": self.click,
            "move_to": self.move_to,
            "drag_to": self.drag_to,
            "type": self.type,
            "press": self.press,
            "scroll": self.scroll,
            "click_item": self.click_item,
            "start_app": self.start_app,
        }
        try:
            with open("./prompts/prompt.txt", "r") as file:
                self.prompt = file.read()
        except FileNotFoundError:
            logging.error("Prompt file not found")

        try:
            with open("./prompts/tools.json", "r") as file:
                self.tools = json.load(file)
        except FileNotFoundError:
            logging.error("Tools file not found")

    def click(self, x: int, y: int, button: str = "left"):
        import pyautogui

        pyautogui.click(x, y, button)
        logging.info(f"Clicked at {x}, {y}")

    def move_to(self, x, y):
        import pyautogui

        pyautogui.moveTo(x, y)

    def drag_to(self, x, y, duration=1):
        import pyautogui

        pyautogui.dragTo(x, y, duration=duration)

    def type(self, text):
        import pyautogui

        pyautogui.typewrite(text)
        logging.info(f"Typed {text}")

    def press(self, keys: str | Iterable[str]):
        import pyautogui

        pyautogui.press(keys)
        logging.info(f"Pressed {keys}")

    def scroll(self, direction, times):
        import pyautogui

        pyautogui.scroll(times * (120 if direction == "up" else -120))

    def click_item(self, item_name):
        import pyautogui

        element = next((e for e in self.item_details if e.name == item_name), None)
        if element:
            x = element.rect.left + (element.rect.right - element.rect.left) / 2
            y = element.rect.top + (element.rect.bottom - element.rect.top) / 2
            pyautogui.click(x, y)
            logging.info(f"Clicked on {item_name} at {x}, {y}")

    def start_app(self, name):
        self.press("win")
        sleep(1)
        self.type(name)
        sleep(1)
        self.press("enter")
        logging.info(f"Started {name}")

    def update_item_details(self):
        window = self.uiautomation_helper.get_foreground_window()
        uia_elements = self.uiautomation_helper.get_element_tree_from_window(window)
        if config["MODE"] == "DEBUG":
            self.uiautomation_helper.screenshot_window_with_masks(window, uia_elements)
        self.item_details = [
            ItemDetail(
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

    def query(self, task):
        self.update_item_details()
        item_briefs = [
            {
                "name": item.name,
                "control_type": item.type,
            }
            for item in self.item_details
        ]
        item_briefs_json = json.dumps(item_briefs)

        query_messages = []
        query_messages.append({"role": "system", "content": self.prompt})
        query_messages.append({"role": "user", "content": "task: " + task})
        query_messages.append(
            {
                "role": "user",
                "content": "operation_history: " + json.dumps(self.operation_history),
            }
        )
        if len(self.operation_history) == 0:
            query_messages.append({"role": "user", "content": "screen ui: " + ""})
        else:
            query_messages.append(
                {"role": "user", "content": "screen ui: " + item_briefs_json}
            )

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=query_messages,
            tools=self.tools,
            tool_choice="auto",
        )
        self.total_completion_tokens += completion.usage.completion_tokens
        self.total_prompt_tokens += completion.usage.prompt_tokens
        return completion

    def run(self, task):
        self.operation_history = []
        self.item_details = []
        try:
            self.is_running = True
            count = 0
            while self.is_running and count < self.max_step:
                completion = self.query(task)
                message = completion.choices[0].message
                if message.tool_calls:
                    function_obj = message.tool_calls[0].function
                    name = function_obj.name
                    args = function_obj.arguments
                    args_json = json.loads(args)
                    function_to_call = self.available_functions[name]
                    function_to_call(**args_json)
                    print({"function": name, "args": args_json})
                    self.operation_history.append({"function": name, "args": args_json})
                elif message.content:
                    print(message.content)
                    break
                else:
                    logging.error("No message content or tool call found")
                    break
                count += 1
                if count == self.max_step:
                    logging.error("Max step reached")
                    break
                sleep(1)
            return "completed"
        except Exception as e:
            logging.error(e)
            return "error"
        finally:
            self.is_running = False
            prompt_cost = (
                self.total_prompt_tokens / 1000 * config["COST_PER_1k_PROMPT_AUTO"]
            )
            completion_cost = (
                self.total_completion_tokens
                / 1000
                * config["COST_PER_1k_COMPLETION_AUTO"]
            )
            self.cost = prompt_cost + completion_cost
            print(
                f"prompt tokens: {self.total_prompt_tokens}\ncompletion tokens:{self.total_completion_tokens}\nprompt cost: {prompt_cost}\ncompletion cost: {completion_cost}\ntotal cost: {self.cost}"
            )
            self.cost = 0
            self.total_prompt_tokens = 0
            self.total_completion_tokens = 0
            logging.info("Operation finished")

    def run_local(self, steps):
        for step in steps:
            function_to_call = self.available_functions[step["function"]]
            self.update_item_details()
            function_to_call(**step["args"])
            sleep(1)
