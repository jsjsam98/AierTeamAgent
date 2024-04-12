import json
import os

from config.config import load_config

config = load_config()


def save_data(data, filename=config["APPDATA_TASK_FILE"]):
    # Get the AppData path from environment variables
    appdata_path = os.getenv("APPDATA")

    # Specify your application's specific folder name
    app_folder_name = config["APP_NAME"]

    # Construct the full path to your application's data folder within AppData
    app_data_path = os.path.join(appdata_path, app_folder_name)

    # Create the directory if it doesn't already exist
    os.makedirs(app_data_path, exist_ok=True)

    # Construct the full path to the file where you'll save the data
    file_path = os.path.join(app_data_path, filename)

    # Write the data to the file as JSON
    with open(file_path, "w") as file:
        json.dump(data, file)

    print(f"Data saved to {file_path}")


def load_data(filename=config["APPDATA_TASK_FILE"]):
    # Get the AppData path from environment variables
    appdata_path = os.getenv("APPDATA")

    # Specify your application's specific folder name
    app_folder_name = config["APP_NAME"]

    # Construct the full path to your application's data folder within AppData
    app_data_path = os.path.join(appdata_path, app_folder_name)

    # Construct the full path to the file where the data is saved
    file_path = os.path.join(app_data_path, filename)

    # Check if the file exists before attempting to load
    if not os.path.exists(file_path):
        print(f"No data file found at {file_path}. Returning empty data.")
        return []  # or return [] if your data is a list

    # Load and return the data from the file
    with open(file_path, "r") as file:
        data = json.load(file)
        print(f"Data loaded from {file_path}")
        return data
