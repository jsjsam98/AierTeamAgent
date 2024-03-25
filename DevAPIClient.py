import logging
import requests
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
import getpass

GPT_INSTRUCT_MODEL = "gpt-3.5-turbo-instruct"
GPT_MODEL = "gpt-4"
GPT_VISION_MODEL = "gpt-4-vision-preview"
OPENAI_API_KEY = getpass.getpass("Enter your OpenAI API key:")

openai_api_key = OPENAI_API_KEY


@retry(wait=wait_random_exponential(multiplier=1, max=20), stop=stop_after_attempt(3))
def completion_request(prompt, model=GPT_INSTRUCT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai_api_key,
    }
    json_data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate Completion response")
        print(f"Exception: {e}")
        return e


@retry(wait=wait_random_exponential(multiplier=1, max=20), stop=stop_after_attempt(3))
def chat_completion_request(messages, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai_api_key,
    }
    json_data = {
        "model": model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0,
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


@retry(wait=wait_random_exponential(multiplier=1, max=20), stop=stop_after_attempt(3))
def chat_vision_completion_request(messages, model=GPT_VISION_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai_api_key,
    }
    json_data = {
        "model": model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0,
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


class DevAPIClient:
    def __init__(self):
        self.open_api_key = openai_api_key
        self.GPT_MODEL = GPT_MODEL
        self.messages = []
        self.prompt = ""
        self.prompt_token_count = 0
        self.completion_token_count = 0
        try:
            with open("./Prompts/prompt_brief.txt", "r") as file:
                self.prompt = file.read()
        except FileNotFoundError:
            self.prompt = ""

        self.messages.append({"role": "system", "content": self.prompt})

        print("key: ", self.open_api_key)

    def reset(self):
        self.messages.clear()
        self.messages.append({"role": "system", "content": self.prompt})

    def get_command(
        self,
        request,
        screenshot="",
    ):
        self.messages.append({"role": "user", "content": screenshot})
        self.messages.append({"role": "user", "content": request})
        logging.info(f"Current Message: {self.messages}")
        request_uri = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.open_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.GPT_MODEL,
            "messages": self.messages,
            "max_tokens": 2000,
            "temperature": 0,
        }

        response = requests.post(request_uri, headers=headers, json=payload)
        response_json = response.json()
        self.prompt_token_count += int(response_json["usage"]["prompt_tokens"])
        self.completion_token_count += int(response_json["usage"]["completion_tokens"])

        content = response_json["choices"][0]["message"]["content"]
        del self.messages[-2]
        self.messages.append({"role": "assistant", "content": content})
        # result = json.loads(content)["command"]
        result = content
        return result
