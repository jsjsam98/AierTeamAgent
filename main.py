from ExecutionAgent import ExecutionAgent
import logging

logging.basicConfig(
    filename="aierteam.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    agent = ExecutionAgent()
    task = input("Enter the task: ")
    agent.search_and_execute(task)


if __name__ == "__main__":
    main()
