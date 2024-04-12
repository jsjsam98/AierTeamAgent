import json
import time
from assistant.OpenAIAssistnat import OpenAIAssistant
from config.config import load_config
from execution.session import MainSession
from openai import OpenAI
from db.service import save_data, load_data

config = load_config()


class MainModel:
    def __init__(self):
        self.session = MainSession()
        #### OPENAI ASSISTANT #####
        self.available_functions = {"run": self.session.run}
        self.assistant = OpenAIAssistant(available_functions=self.available_functions)
        ###########################
        self.messages = []
        self.tasks = []
        self.load_tasks()

    def add_message(self, text):
        self.messages.append({"role": "user", "content": text})
        message = self.assistant.add_message(text)
        self.messages.append(message)
        if len(self.session.operation_history) > 0:
            self.tasks.append(
                {
                    "task": self.session.task,
                    "steps": self.session.operation_history,
                }
            )
            self.session.clear_task()
            self.save_tasks()
        # message = self.client.beta.threads.messages.create(
        #     thread_id=self.thread.id,
        #     role="user",
        #     content=text,
        # )
        # run = self.client.beta.threads.runs.create_and_poll(
        #     thread_id=self.thread.id,
        #     assistant_id=self.assistant.id,
        # )

        # if run.status == "completed":
        #     # use the default limit = 20
        #     messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        #     response_message = messages.data[0].content[0].text.value
        #     self.messages.append({"role": "assistant", "content": response_message})
        # elif run.status == "requires_action":
        #     required_action = run.required_action
        #     tool_call = required_action.submit_tool_outputs.tool_calls[0]
        #     function_obj = tool_call.function
        #     name = function_obj.name
        #     args = function_obj.arguments
        #     args_json = json.loads(args)
        #     function_to_call = self.available_functions[name]
        #     function_to_call_result = function_to_call(**args_json)
        #     run = self.client.beta.threads.runs.submit_tool_outputs(
        #         thread_id=self.thread.id,
        #         run_id=run.id,
        #         tool_outputs=[
        #             {
        #                 "tool_call_id": tool_call.id,
        #                 "output": function_to_call_result,
        #             }
        #         ],
        #     )
        #     run = self.wait_on_run(run, self.thread)
        #     if run.status == "completed":
        #         # use the default limit = 20
        #         messages = self.client.beta.threads.messages.list(
        #             thread_id=self.thread.id
        #         )
        #         response_message = messages.data[0].content[0].text.value
        #         self.messages.append({"role": "assistant", "content": response_message})
        #         self.tasks.append(
        #             {"task": args_json["task"], "steps": self.session.operation_history}
        #         )
        # else:
        #     self.messages.append(
        #         {"role": "assistant", "content": "AI is not available"}
        #     )

    def load_tasks(self):
        self.tasks = load_data()

    def save_tasks(self):
        save_data(self.tasks)
