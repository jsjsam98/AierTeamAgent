from ExecutionAgent import ExecutionAgent
import pyautogui
import logging

logging.basicConfig(
    filename="aierteam.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
agent = ExecutionAgent()
task = input("Enter the task: ")
agent.search_and_execute(task)
