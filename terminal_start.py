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

    mode = sys.argv[1]
    task = sys.argv[2]  

    session = MainSession()

    if mode == '-mode text':
        session.run(task)
    elif mode == '-mode vision':
        session.run_vision_mode(task)
    else:
        print("Invalid mode. Please use -mode text or -mode vision.")
        sys.exit(1)

if __name__ == "__main__":
    main()
