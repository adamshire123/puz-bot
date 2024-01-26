import json
import logging
import os

from google.cloud import pubsub_v1

from slack_bolt import App
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler

logging.basicConfig(level=logging.INFO)

# process_before_response must be True when running on FaaS
app = App(process_before_response=True, signing_secret=os.getenv("SIGNING_SECRET"), token=os.getenv("BOT_TOKEN"))


# for testing
@app.command("/hello")
def hello_command(body, say, ack):
    logging.info(body)
    ack()
    say("Hi from Google Cloud Functions!")

# for testing
@app.event("app_mention")
def event_test(body, say, ack):
    logging.info(body)
    ack()
    say("Hi from Google Cloud Functions!")

# kick off new puzzle creation
@app.command("/init")
def initialize_puzzle(body, say, ack):
    ack('initializing puzzle...')
    if body['text']:
        send_pub_sub(body)
    else:
        say("please provide a puzzle name: e.g. puz-salad-daze")


handler = SlackRequestHandler(app)

# Cloud Function Entry Point
def cloud_function_handler(req):
   
    return handler.handle(req)

def send_pub_sub(data):

    project_id = os.getenv("PROJECT_ID")
    topic_id = os.getenv("PUBSUB_TOPIC")

    publisher = pubsub_v1.PublisherClient()
   
    topic_path = publisher.topic_path(project_id, topic_id)

    future = publisher.publish(topic_path, data=json.dumps(data).encode("utf8"))
    
    logging.info(future.result())
    logging.info(f"Published message to {topic_path}.")