from openai import OpenAI
from flask import current_app
from apiflask import abort as flask_abort

AI_INSTRUCTIONS = "Please address the user as Jane Doe. The user has a premium account."

CLIENT = OpenAI(
  organization=current_app.config['ORGANIZATION'],
  project=current_app.config['PROJECT'],
  api_key = current_app.config['API_KEY']
)

def send_message_to_llm(weather_data, client_object=CLIENT):
  # this is used to establish a connection with the assistant
  client_object.beta.assistants.retrieve(current_app.config['ASSISTANT_ID'])
  thread = client_object.beta.threads.create()

  # send the user data, in our case the weather data, to openai, but do not yet make any changes.
  client_object.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=weather_data
  )

  # only with this command, the message gets actually interpreted and processed.
  run = client_object.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=current_app.config['ASSISTANT_ID'],
    instructions=AI_INSTRUCTIONS
  )

  # check if the status is completed, if not i will abort the flask request.
  if run.status == 'completed': 
    messages = client_object.beta.threads.messages.list(thread_id=thread.id)
    return messages
  else:
    flask_abort(500, run.status)
