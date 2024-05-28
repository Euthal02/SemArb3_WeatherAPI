from openai import OpenAI
from flask import current_app

client = OpenAI(
  organization=current_app.config['ORGANIZATION'],
  project=current_app.config['PROJECT'],
  api_key = current_app.config['API_KEY']
)

client.beta.assistants.retrieve(current_app.config['ASSISTANT_ID'])

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=current_app.config['ASSISTANT_ID'],
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)
