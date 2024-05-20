import logging
import sys
from execution.session import MainSession


logging.basicConfig(
    filename="aierteam.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    if len(sys.argv) < 2:
        print("Please provide a command to run.")
        sys.exit(1)

    command_to_run = sys.argv[1]  # Get the first command-line argument
    session = MainSession()
    session.run(command_to_run)


if __name__ == "__main__":
    main()
