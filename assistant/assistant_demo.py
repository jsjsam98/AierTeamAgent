from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.retrieve("asst_44Sz1K0kq6TQ7DBw1IQZk95V")

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id, role="user", content="I want to open a control panel"
)
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Sam",
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages)

elif run.status == "requires_action":
    print(run.required_action)
    print(run.required_action.submit_tool_outputs.tool_calls[0].function)
