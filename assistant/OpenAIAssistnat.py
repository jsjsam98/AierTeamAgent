import json
import time
from openai import OpenAI
from config.config import load_config

config = load_config()


class OpenAIAssistant:
    def __init__(self, thread, available_functions):
        self.client = OpenAI(api_key=config["OPENAI_API_KEY"])
        if "CHAT_ASSISTANT_ID" in config:
            self.assistant = self.client.beta.assistants.retrieve(
                config["CHAT_ASSISTANT_ID"]
            )
        else:
            # create a new assistant
            with open("prompts/prompt_assistant.txt", "r") as file:
                prompt_assistant = file.read()

            with open("prompts/tools_assistant.json", "r") as file:
                tools_assistant = json.load(file)

            # upload files
            uploaded_file = self.client.files.create(
                file=open("knowledge/support.txt", "r"),
                purpose="assistants",
            )

            self.assistant = self.client.beta.assistants.create(
                name="AierTeam Assistant",
                instructions=prompt_assistant,
                tools=tools_assistant,
                model=config["ASSISTANT_MODEL"],
                file_ids=[uploaded_file.id],
            )
        self.messages = []
        self.thread = thread
        self.available_functions = available_functions

    def wait_on_run(self, run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def add_message(self, text):
        self.messages.append({"role": "user", "content": text})
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=text,
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        if run.status == "completed":
            # use the default limit = 20
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            response_message = messages.data[0].content[0].text.value
            self.messages.append({"role": "assistant", "content": response_message})
            return {"role": "assistant", "content": response_message}
        elif run.status == "requires_action":
            required_action = run.required_action
            tool_call = required_action.submit_tool_outputs.tool_calls[0]
            function_obj = tool_call.function
            name = function_obj.name
            args = function_obj.arguments
            args_json = json.loads(args)
            function_to_call = self.available_functions[name]
            function_to_call_result = function_to_call(**args_json)
            run = self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call.id,
                        "output": function_to_call_result,
                    }
                ],
            )
            run = self.wait_on_run(run, self.thread)
            if run.status == "completed":
                # use the default limit = 20
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                response_message = messages.data[0].content[0].text.value
                self.messages.append({"role": "assistant", "content": response_message})
                # self.tasks.append(
                #     {"task": args_json["task"], "steps": self.session.operation_history}
                # )
                return {"role": "assistant", "content": response_message}
        else:
            self.messages.append(
                {"role": "assistant", "content": "Assistant not available"}
            )