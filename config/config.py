import os
import yaml
import json

config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

print(config_file_path)


def load_config():
    """Load configuration from a YAML file."""
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    config = load_config()
    print(config["ASSISTANT_ID"])
